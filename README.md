# virtual-piano
For the people who thinks the real one is too expensive

## **Multi-functional piano**

### ***Keyboard inputs***

![image](https://user-images.githubusercontent.com/17162465/137605327-787a1ad5-2621-4267-acc5-a11ef20b408a.png)

### ***Graphical user interface input description***

![image](https://user-images.githubusercontent.com/17162465/137605375-7401103b-7d79-43d1-829c-7f6798f8088b.png)


### ***Waveforms***
- There are 4 options for selecting waveform :
 -- Type1 :- Square wave, Triangle wave, Sawtooth wave.
 -- Type2 :- White noise( 1 Hz < frequency< 20,000 Hz).
 -- Default is Sawtooth wave.
- tick on the corresponding waveform.
- There is an option for no.of Harmonics (default is 20) used to make Type1 waveforms from sine waves.
- If you select Type1 waveform then the input is required from the keyboard, different keyboard buttons will produce a waveform of corresponding frequencies(see keyboard section above), you can press one or more buttons simultaneously. It will produce the sum of the corresponding waveforms whose buttons are pressed.
- If you select Noise, then it will take some time to process and then produce a waveform for 6 seconds. No need to give input from keyboard.

## You can apply :-
1. ADSR envelope.
2. Filters (with constant or time-dependent cutoff frequency).
3. Equalization
4. Amplitude modulation.
5. Frequency modulation.
On all waveforms ( you can also apply all these together ).

### 1. ***ADSR Envelope***

![image](https://user-images.githubusercontent.com/17162465/137606543-da37309a-6c27-48e1-8eda-c2a0c2a657f4.png)

You can envelop your waveform using ADSR parameters:-

- There are 3 inputs for attack time (default is 10 ), decay time (default is 3000) and release time (default is 10) .Note :- All inputs should be in msec.
- There is a slider for sustain level (in dB) :- 0 dB implies sustain hight = volume ( default is -10 dB ).
- First it will be in attack mode, then it will be in decay mode for the specified time by the user then will remain in the sustain level as long as the key is pressed. When key is released then it will come down through release mode.

### 2. ***Filters***

- There are 3 options for selecting filters :
-- Lowpass filter.
-- Highpass filter.
-- Bandpass filter.
Note : you have to select bandpass filter if you want equalization ( see Equalization section).

- Tick the box to select corresponding filter.
- There is an option for the order of filter (default is 10).
Note :- All filters are butterworth.

- You can put the cutoff frequency of the filter which you have picked (central frequency in case of bandpass filter), in two ways :-
-- Constant :- you can give it via fix cutoff frequency option.
-- Time dependent :- you can give it via 2 options- **lower frequency** and **higher frequency**. In this case, the cutoff frequency will vary from lower to higher frequency sinusoidally with 0.5 Hz frequency.

- There is an option for BandWidth of bandpass filter ( default is 100 ).


### 3. ***Equalization***
![image](https://user-images.githubusercontent.com/17162465/137606659-9de6325b-21da-450f-9143-8f38c524cd44.png)

- You need to select bandpass filter to do equalization.
- Band width and central frequency for it is the same as that for bandpass filter ( see filter section ).
- There is a slider for volume at equalizing frequency ( in dB).
-- > 0 implies frequency will boost around central frequency.
-- < 0 implies frequency will cut around central frequency.
-- = 0 implies equalization will not happen.

### 4. ***Amplitude Modulation***
- There are 2 parameters required for amplitude modulation.
- There is an option for Amplitude modulation frequency.
Note :- It will not do amplitude modulation if this text is empty.
- There is a slider for Amplitude modulation depth ( in dB) :- default value is -20 dB.

### 5. ***Frequency Modulation***
- There is an option for FM frequency ratio ( modulating frequency = freq x frequency ratio ).
Note:- It will not do frequency modulation if this text is empty.
- There is a slider for Frequency modulation depth ( 0-50 Hz):- default is 20 Hz.
- There is another slider for FM depth changing amplitude (0-100 Hz). This is again changing the frequency modulation depth sinusoidally.




## ***Installation***
- sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
- sudo pip install pyaudio
- sudo apt-get install python3-tk
- sudo pip install numpy
- sudo pip install matplotlib
