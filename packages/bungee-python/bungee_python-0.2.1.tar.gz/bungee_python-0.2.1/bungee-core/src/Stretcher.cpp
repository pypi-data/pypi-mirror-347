// Copyright (C) 2020-2025 Parabola Research Limited
// SPDX-License-Identifier: MPL-2.0

#define BUNGEE_BASIC_CPP

#include "Stretcher.h"
#include "Assert.h"
#include "Instrumentation.h"
#include "Resample.h"
#include "Synthesis.h"
#include "log2.h"

namespace Bungee {

Internal::Stretcher::Stretcher(SampleRates sampleRates, int channelCount, int log2SynthesisHopAdjust) :
	Timing(sampleRates, log2SynthesisHopAdjust),
	transforms(Fourier::transforms()),
	input(log2SynthesisHop, channelCount, *transforms),
	grains(4),
	output(*transforms, log2SynthesisHop, channelCount, maxOutputFrameCount(true), 0.25f, {1.f, 0.5f})
{
	for (auto &grain : grains.vector)
		grain = std::make_unique<Grain>(log2SynthesisHop, channelCount);
}

InputChunk Internal::Stretcher::specifyGrain(const Request &request, double bufferStartPosition)
{
	Instrumentation::Call call(this, 0);
	const Assert::FloatingPointExceptions floatingPointExceptions(0);

	grains.rotate();

	auto &grain = grains[0];
	auto &previous = grains[1];

	return grain.specify(request, previous, sampleRates, log2SynthesisHop, bufferStartPosition);
}

void Internal::Stretcher::analyseGrain(const float *data, std::ptrdiff_t stride, int muteFrameCountHead, int muteFrameCountTail)
{
	Instrumentation::Call call(this, 1);
	const Assert::FloatingPointExceptions floatingPointExceptions(FE_INEXACT | FE_UNDERFLOW | FE_DENORMALOPERAND);

	auto &grain = grains[0];
	const auto &previous = grains[1];

	if (Instrumentation::threadLocal->logCount == 0)
		Instrumentation::log("Stretcher: sampleRates=[%d, %d] channelCount=%d  synthesisHop=%d", sampleRates.input, sampleRates.output, input.windowedInput.cols(), 1 << log2SynthesisHop);
	Instrumentation::log("analyseGrain: position=%f speed=%f pitch=%f reset=%s data=%p stride=%d mute=%d:%d", grain.request.position, grain.request.speed, grain.request.pitch, grain.request.reset ? "true" : "false", data, stride, muteFrameCountHead, muteFrameCountTail);

	grain.muteFrameCountHead = muteFrameCountHead;
	grain.muteFrameCountTail = muteFrameCountTail;

	grain.validBinCount = 0;
	if (grain.valid())
	{
		auto m = grain.inputChunkMap(data, stride, muteFrameCountHead, muteFrameCountTail, previous);

		auto ref = grain.resampleInput(m, 8 << log2SynthesisHop, muteFrameCountHead, muteFrameCountTail);

		auto log2TransformLength = input.applyAnalysisWindow(ref, muteFrameCountHead, muteFrameCountTail);

		transforms->forward(log2TransformLength, input.windowedInput, grain.transformed);

		const auto n = Fourier::binCount(grain.log2TransformLength) - 1;
		grain.validBinCount = std::min<int>(std::ceil(n / grain.resampleOperations.output.ratio), n) + 1;
		grain.transformed.middleRows(grain.validBinCount, n + 1 - grain.validBinCount).setZero();

		grain.log2TransformLength = log2TransformLength;

		for (int i = 0; i < grain.validBinCount; ++i)
		{
			const auto x = grain.transformed.row(i).sum();
			grain.energy[i] = x.real() * x.real() + x.imag() * x.imag();
			grain.phase[i] = Phase::fromRadians(std::arg(x));
		}

		Partials::enumerate(grain.partials, grain.validBinCount, grain.energy);

		if (grain.continuous)
			Partials::suppressTransientPartials(grain.partials, grain.energy, grains[1].energy);
	}
}

void Internal::Stretcher::synthesiseGrain(OutputChunk &outputChunk)
{
	Instrumentation::Call call(this, 2);

	const Assert::FloatingPointExceptions floatingPointExceptions(FE_INEXACT);

	auto &grain = grains[0];
	if (grain.valid())
	{
		auto n = Fourier::binCount(grain.log2TransformLength);

		BUNGEE_ASSERT1(!grain.passthrough || grain.analysis.speed == grain.passthrough);

		Synthesis::synthesise(log2SynthesisHop, grain, grains[1]);

		BUNGEE_ASSERT2(!grain.passthrough || grain.rotation.topRows(grain.validBinCount).isZero());

		auto theta = grain.rotation.topRows(grain.validBinCount).cast<float>() * (std::numbers::pi_v<float> / 0x8000);
		auto t = theta.cos() + theta.sin() * std::complex<float>{0, 1};
		if (grain.reverse())
			grain.transformed.topRows(grain.validBinCount) = grain.transformed.topRows(grain.validBinCount).conjugate().colwise() * t;
		else
			grain.transformed.topRows(grain.validBinCount).colwise() *= t;

		transforms->inverse(grain.log2TransformLength, output.inverseTransformed, grain.transformed);
	}

	output.applySynthesisWindow(log2SynthesisHop, grains, output.synthesisWindow);

	Output::Segment::lapPadding(grains[3].segment, grains[2].segment);

	outputChunk = grains[3].segment.resample(
		output.resampleOffset,
		grains[2].resampleOperations.output,
		grains[1].resampleOperations.output,
		output.bufferResampled);

	outputChunk.request[OutputChunk::begin] = &grains[2].request;
	outputChunk.request[OutputChunk::end] = &grains[1].request;
}

extern const char *versionDescription;
} // namespace Bungee

const Bungee::Functions *getFunctionsBungeeBasic()
{
	static const char *edition = "Basic";
	static const Bungee::Internal::Functions<Bungee::Internal::Stretcher, &edition, &Bungee::versionDescription> functions{};
	return &functions;
}
