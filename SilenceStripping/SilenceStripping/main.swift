//
//  main.swift
//  SilenceStripping
//
//  Created by Ryan Purpura on 1/31/20.
//  Copyright © 2020 Ryan Purpura. All rights reserved.
//


import Foundation
import AVFoundation

let url = URL(fileURLWithPath: "/Users/rpurp/pdev/SilenceStripping/SilenceStripping/cs189.mp3")
let outURL = URL(fileURLWithPath: "/Users/rpurp/Desktop/out.aac")

let outputFormatSettings = [
    AVFormatIDKey: kAudioFormatMPEG4AAC,
    AVSampleRateKey: Float64(44100)
    ] as [String : Any]

let bufferFormatSettings = [
    AVFormatIDKey: kAudioFormatLinearPCM,
    AVLinearPCMBitDepthKey: 32,
    AVLinearPCMIsFloatKey: true,
    AVSampleRateKey: Float64(44100),
    AVNumberOfChannelsKey: 1
    ] as [String : Any]

let audioFile = try AVAudioFile(forReading: url)
let outAudioFile = try AVAudioFile(forWriting: outURL, settings: outputFormatSettings, commonFormat: .pcmFormatFloat32, interleaved: false)

let outputFrameCapacity: UInt32 = 44100 * 60
let inputFrameCapacity: UInt32 = 500

let inputBuffer = AVAudioPCMBuffer(pcmFormat: AVAudioFormat(settings: bufferFormatSettings)!, frameCapacity: inputFrameCapacity)!
let outputBuffer = AVAudioPCMBuffer(pcmFormat: AVAudioFormat(settings: bufferFormatSettings)!, frameCapacity: outputFrameCapacity)!
let outputChannelData = outputBuffer.floatChannelData!.pointee

print("Starting...")

var shouldCrossfade = false
let crossFadeLength: UInt32 = 1

var count: UInt32 = 0

while audioFile.framePosition < audioFile.length {
    
    try audioFile.read(into: inputBuffer, frameCount: inputFrameCapacity)
    let inputChannelData = inputBuffer.floatChannelData!.pointee
    
    var sum: Float32 = 0
    for i in 0..<inputFrameCapacity {
        sum += abs(inputChannelData[Int(i)])
    }
    
    if sum / Float32(inputFrameCapacity) > 0.01 {
        for i in 0..<inputFrameCapacity {
            if i < crossFadeLength && shouldCrossfade {
                
                let fadeAmount = sqrt(Float32(1/2 * (1 + i / crossFadeLength)))
                outputChannelData[Int(count)] += inputChannelData[Int(i)] * fadeAmount
            } else {
                outputChannelData[Int(count)] = inputChannelData[Int(i)]
                count += 1
            }
        }
        shouldCrossfade = false
        if count >= outputFrameCapacity - inputFrameCapacity {
            outputBuffer.frameLength = UInt32(count)
            try outAudioFile.write(from: outputBuffer)
            count = 0
            print("One minute done.")
        }
        
    } else if !shouldCrossfade {
        for i in 0..<crossFadeLength {
            let fadeAmount = sqrt(Float32(1/2 * (1 - i / crossFadeLength)))
            outputChannelData[Int(count)] = inputChannelData[Int(i)] * fadeAmount
            count += 1
        }
        count -= crossFadeLength
        shouldCrossfade = true
    }
    
}

outputBuffer.frameLength = UInt32(count)
try outAudioFile.write(from: outputBuffer)
count = 0


print("Done")
