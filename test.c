#define DR_WAV_IMPLEMENTATION
#include "fft.h"
#include "dr_wav.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define NUM 4096



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
	Fft_transform(real, imag, size);

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
    plotFrequency("RES", real, im, NUM);
	//double r[NUM];
	//double i[NUM];
	//readDataFromFile("DATA", r, NUM);
	//plotFrequency("RES", r, i, NUM);
	return 0;

}
