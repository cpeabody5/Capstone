#define DR_WAV_IMPLEMENTATION
#include "fft.h"
#include "dr_wav.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define SAMPLEFREQUENCY 44100
#define NUM_SAMPLES 44100 * 1

typedef struct filter
{
	int order;
	double *coeff;
}filter_t;

/*
Create an array of filter coefficents for the given frequency requirements 
Inputs: 
lowFreq - low frequency requirement, input 0 for lowpass filter
highFreq - high frequency requirement
filter - struct for filter to be defined
Output:
return 0 on error
*/
int createFilter(int lowFreq, int highFreq, filter_t *filter)
{
	return 0;
}

/*
Filter the data in real and imag using a filter defined by coeff and order 
Inputs: 
filter - filter struct to be used  
real and imag and arrays of input data
size - the size of real and imag arrays
Output:
return 0 on error
*/
int filterData(filter_t * filter, double real[], double imag[], int size)
{
	return 0;
}

//Reads filename.wav into specified buffer
//Returns 0 if failed to read file, returns total number of samples 
int readDataFromWav(const char* filename, float buff[], unsigned int* sampleRate, drwav_uint64* totalPCMFrameCount){
	unsigned int channels;
    float * pSampleData = drwav_open_file_and_read_pcm_frames_f32(filename, &channels, sampleRate, totalPCMFrameCount, NULL);
	//printf("File Info:\n\tsampleRate = %d\n\tchannels = %d\n\tpcmframecount = %llu\n", sampleRate, channels, totalPCMFrameCount);
    if (pSampleData == NULL) {
        // Error opening and reading WAV file.
        return 0;
    }

    for(unsigned long long i = 0; i < *totalPCMFrameCount; i++)	buff[i] = (*(pSampleData+i));

    //drwav_free(buff, NULL);
    return 1;
}

/*
Inputs:
buff is a data buffer
filename is the path of the file to be read
Outputs:
returns 1 on successful read 0 on error
*/
int readDataFromFile(const char* filename, double buff[], int size)
{
	FILE* in_f;
	if((in_f = fopen(filename, "r")))
	{
		double data;
		int i = 0;
		int in = fscanf(in_f, "%lf", &data);
		while(in != EOF && i < size)
		{
			buff[i] = data;
			in = fscanf(in_f, "%lf", &data);
			i++;
		}
		fclose(in_f);
		return 1;
	}
	else return 0;
}



int plotFrequency(const char* filename, double real[], double imag[], int size)
{

	FILE* out_f; 

	if((out_f = fopen(filename,"w"))){
		double w = 0;
		double dw = 44100.0/size;
		double H;
		for(int i = 0; i <= size; i++)
		{
			H = sqrt(real[i]*real[i] + imag[i]*imag[i])/size;
			H = (H>10000)?10000:H;
			fprintf(out_f, "%f\t%f\n", w, H);
			w+=dw;
		}
		fclose(out_f);
		return 1;
	}
	return 0;
}

int main(int argc, char* argv[])
{	
	printf("Declaring variables\n\n");
	float window_sec = 0.2;	// Number of seconds in analysis window
	unsigned int window_samples;	// Number of samples in analysis window
	
	// For WAV
	drwav_uint64 total_samples;
	unsigned int sampleRate;
	unsigned int channels;

	// Read audio file to buffer
	//readDataFromWav(argv[1], audio_samples, &sampleRate, &total_samples);
    float * audio_samples = drwav_open_file_and_read_pcm_frames_f32(argv[1], &channels, &sampleRate, &total_samples, NULL);
	if (audio_samples == NULL) return 1;	// Error reading audio file
	
	printf("Finished reading from file: %s, number of samples read = %llu\n, sampleRate = %d\n\n", argv[1], total_samples, sampleRate);

	// Calculate Number of Samples in analysis window based on sampling rate
	window_samples = (unsigned int) (window_sec * sampleRate);

	// Init Real and Im arrays
	// real = (double*) malloc(window_samples * sizeof(double));
	// im = (double*) malloc(window_samples * sizeof(double));
	

	// Go through samples in frames of a specified window length (window_samples)
	int i;
	int j;
	for (i = 0; i < total_samples; i += window_samples) {
		double real[window_samples];
		double im[window_samples];

		printf("%f\n", im[20]);

		for(int k = 0; k < window_samples; k++){
			im[k] = 0;
			real[k] = 0;
		}
		
		// Get current window (sub-array of total audio samples)
		for(j = i; j < i + window_samples; j++) {
			if (j > total_samples) {
				break;
			}
			real[j - i] = audio_samples[j];
		}

		// Perform FFT on current frame
		Fft_transform(real, im, window_samples);

		// Save Data to File
		char outFilename[64];
		sprintf(outFilename, "data/RES_%d", i/window_samples);
		printf("Saving Data of iteration %d to file %s\n", i/window_samples, outFilename);
		plotFrequency(outFilename, real, im, window_samples);
	}

	return 0;
}
