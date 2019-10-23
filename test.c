#define DR_WAV_IMPLEMENTATION
#include "fft.h"
#include "dr_wav.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define NUM 4096
#define SAMPLEFREQUENCY 44100

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

//Reads numSamples from filename into buff
//Returns 0 if failed to read file
int readDataFromWav(const char* filename, double buff[], int numSamples){
	unsigned int channels;
    unsigned int sampleRate;
    drwav_uint64 totalPCMFrameCount;
    float* pSampleData = drwav_open_file_and_read_pcm_frames_f32(filename, &channels, &sampleRate, &totalPCMFrameCount, NULL);
    if (pSampleData == NULL) {
        // Error opening and reading WAV file.
        return 0;
    }

    for(int i = 0; i < numSamples; i++)	buff[i] = (*(pSampleData+i));

    drwav_free(pSampleData, NULL);
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
			H = sqrt(real[i]*real[i] + imag[i]*imag[i]);
			H = (H>10000)?10000:H;
			fprintf(out_f, "%f\t%f\n", w, H);
			w+=dw;
		}
		fclose(out_f);
		return 1;
	}
	return 0;
}

int main()
{
	double real[NUM];
	double im[NUM] = {};

	readDataFromWav("sine1000.wav", real, NUM);

    Fft_transform(real, im, NUM);

    plotFrequency("RES", real, im, NUM);


	return 0;
}
