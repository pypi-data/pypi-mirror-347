// Copyright (C) 2020-2025 Parabola Research Limited
// SPDX-License-Identifier: MPL-2.0

#include <bungee/Bungee.h>
#include <bungee/CommandLine.h>
#include <bungee/Stream.h>

int main(int argc, const char *argv[])
{
	using namespace Bungee;

	Request request{};
#ifndef BUNGEE_EDITION
#	define BUNGEE_EDITION Basic
#endif
	typedef BUNGEE_EDITION Edition;

	static const auto helpString = std::string("Bungee ") + Bungee::Stretcher<Edition>::edition() + " audio speed and pitch changer\n\n" +
		"Version: " + Bungee::Stretcher<Edition>::version() + "\n";

	CommandLine::Options options{"<bungee-command>", helpString};
	CommandLine::Parameters parameters{options, argc, argv, request};
	CommandLine::Processor processor{parameters, request};

	Bungee::Stretcher<Edition> stretcher(processor.sampleRates, processor.channelCount, parameters["grain"].as<int>());

	stretcher.enableInstrumentation(parameters["instrumentation"].count() != 0);

	const int pushSampleCount = parameters["push"].as<int>();
	if (pushSampleCount)
	{
		// This code demonstrates the usage of the easier to use, positive-speed-only `Bungee::Stream` API.
		// See the `else` branch for equivalent usage of the `Bungee::Stretcher` API.

		const auto maxSpeed = request.speed;

		if (pushSampleCount < 0)
			std::cout << "Using Bungee::Stream::process randomly with between 1 and " << -pushSampleCount << " samples per call\n";
		else
			std::cout << "Using Bungee::Stream::process with " << pushSampleCount << " samples per call\n";

		const int maxInputSampleCount = std::abs(pushSampleCount);
		const int maxOutputSampleCount = std::ceil((maxInputSampleCount * processor.sampleRates.output) / (maxSpeed * processor.sampleRates.input));

		CommandLine::Processor::OutputChunkBuffer outputChunkBuffer(maxOutputSampleCount, processor.channelCount);

		Stream stream(stretcher, maxInputSampleCount, processor.channelCount);

		std::vector<const float *> inputChannelPointers(processor.channelCount);

		bool done = false;
		for (int position = 0; !done;)
		{
			// Here we loop over segments of input audio, and we control their lengths.
			int inputSampleCount = pushSampleCount < 0 ? std::rand() % maxOutputSampleCount + 1 : pushSampleCount;

			for (int c = 0; c < processor.channelCount; ++c)
				inputChannelPointers[c] = &processor.inputBuffer[position + c * processor.inputChannelStride];

			if (inputSampleCount > processor.inputFrameCount - position)
			{
				if (position < processor.inputFrameCount)
					inputSampleCount = processor.inputFrameCount - position; // shorter last segment of real audio
				else
					for (int c = 0; c < processor.channelCount; ++c)
						inputChannelPointers[c] = nullptr; // indicates silent segment
			}

			const double outputSampleCountIdeal = (inputSampleCount * processor.sampleRates.output) / (request.speed * processor.sampleRates.input);

			// This is the important line: it is a very simple streaming interface.
			const auto outputSampleCountActual = stream.process(inputChannelPointers[0] ? inputChannelPointers.data() : nullptr, outputChunkBuffer.channelPointers.data(), inputSampleCount, outputSampleCountIdeal, request.pitch);

			if (false)
				std::cout << "current latency is " << stream.latency() / processor.sampleRates.input << "seconds\n";

			const auto positionEnd = stream.outputPosition();
			const auto positionBegin = positionEnd - outputSampleCountActual * (request.speed * processor.sampleRates.input / (processor.sampleRates.output));

			auto outputChunk = outputChunkBuffer.outputChunk(outputSampleCountActual, positionBegin, positionEnd);
			done = processor.write(outputChunk);

			position += inputSampleCount;
		}
	}
	else
	{
		// This code demonstrates the low-level, flexible and best performing `Bungee::Stretcher` API.

		processor.restart(request);
		stretcher.preroll(request);

		for (bool done = false; !done;)
		{
			InputChunk inputChunk = stretcher.specifyGrain(request);

			const auto muteFrameCountHead = std::max(0, -inputChunk.begin);
			const auto muteFrameCountTail = std::max(0, inputChunk.end - processor.inputFrameCount);

			stretcher.analyseGrain(processor.getInputAudio(inputChunk), processor.inputChannelStride, muteFrameCountHead, muteFrameCountTail);

			OutputChunk outputChunk;
			stretcher.synthesiseGrain(outputChunk);

			stretcher.next(request);

			done = processor.write(outputChunk);
		}
	}

	processor.writeOutputFile();

	return 0;
}
