from __future__ import division
from pyaudio import PyAudio
from tkinter import *
import pygame
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plot
import random
sample_rate=10000

#function to play the sound

def fetch(ents):
	def sound(y): 
		my=max(y)
		if my>1:
			y=y/my
		samples = ( int(k*127 +128) for k in y  )
		for buf in zip(*[samples]): 
			stream.write(bytes(bytearray(buf)))

	ent=[]
	for i in range(0,24):
		ent.append(ents[i].get())
	if(ent[0]==''): #no.of Harmonics
		ent[0] ='25'
	if(ent[1]==''): #attack time in msec
		ent[1] ='5'
	if(ent[2]==''):
		ent[2] ='3000' #decay time in msec
	if(ent[3]==''):
		ent[3] ='5'
	if(ent[7]==''):
		ent[7] ='10'
	if(ent[11]==''):
		ent[11] ='100' 
	if(ent[16]==''):
		ent[16] ='0' 
	if(ent[18]=='' or ent[18]=='0'):
		fmod_freq_ratio =0
	else:
		fmod_freq_ratio=1/int(ent[18]) 
	if(ent[20]==''):
		ent[20] ='0' 
	if(ent[21]==''):
		ent[21] ='0' 
	harmonics= int(ent[0]) 
	attack=float(ent[1])
	attack=attack/1000
	decay=float(ent[2])
	decay=decay/1000
	dt=10/1000
	release=float(ent[3])
	release=release/1000
	square=ent[4]
	triangle=ent[5]
	sawtooth=ent[6]
	order=int(ent[7])
	lowpass=ent[8]
	highpass=ent[9]
	bandpass=ent[10]
	band_width=int(ent[11])
	sh=np.math.exp(2.303*int(ent[13])/20)
	vol=0.2*np.math.exp(2.303*int(ent[14])/20)
	amod_freq=int(ent[16])
	amod_depth=np.math.exp(2.303*int(ent[17])/20)
	fmod_depth=np.math.exp(2.303*int(ent[19])/20)/2
	low_freq=int(ent[20])
	high_freq=int(ent[21])
	if ent[15]!='':
		cutoff=float(ent[15])
		make_variable=0
	else: make_variable=1
	fmod_depth_change=fmod_depth*int(ent[22])/100
	noise=ent[23]

	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Music synthesizer')
	pygame.mouse.set_visible(1)

	done = False
	clock = pygame.time.Clock()
	#print(type(triangle))
	#For waveform
	a=[]
	if(sawtooth):
		i=1
		a.append(0)
		for j in range(1,harmonics+1):
			a.append(i/(np.pi*j))
			i=(-1)*i
	elif(triangle):
		i=1

		a.append(0)
		for j in range(1,harmonics+1):
			if(j%2 !=0):
				a.append(8*i/(np.pi*np.pi*j*j))
				i=(-1)*i
			else:
				a.append(0)
	else:
		a.append(0)
		for j in range(1,harmonics+1):
			if(j%2 !=0):
				a.append(4/(np.pi*j))
			else:
				a.append(0)

	#Filter function
	if bandpass :
		expm1=np.math.expm1(2.303*int(ent[12])/20)
	def mod_H(f,cutoff):
		if(lowpass):
			h=1/np.sqrt(1 + pow(f/cutoff,2*order))
		elif(highpass):
			h=1/np.sqrt(1 + pow(cutoff/f,2*order))
		elif bandpass  and int(ent[12])==0 :
			h=1/np.sqrt(1 + pow(2*(f-cutoff)/band_width,2*order))
		elif bandpass  and int(ent[12])!=0  :
			h=expm1/np.sqrt(1 + pow(2*(f-cutoff)/band_width,2*order)) + 1
		else: h=1
		return h

	t1 = np.arange(0, attack+dt, 1/sample_rate) #creating time array
	t2 = np.arange(0.0, dt, 1/sample_rate) #creating time array
	t3 = np.arange(0.0, release, 1/sample_rate) #creating time array
	t4 = np.arange(0.0, 6, 1/sample_rate) #creating time array
	p = PyAudio()
	stream = p.open(format=p.get_format_from_width(1),channels=1,rate=sample_rate,output=True)

	#for noise
	if noise:
		rand=[]
		y2=0
		for i in range(0,500):
			rand.append(random.random())
		if make_variable:
			cutoff=(low_freq+high_freq)/2-(high_freq-low_freq)*np.cos(np.pi*t4)/2
		for i in range(1,500):
			y2=y2+mod_H(10*i,cutoff)*np.sin(2*np.pi*(10*i)*t4+2*np.pi*rand[i]+(fmod_depth+fmod_depth_change*np.sin(2*np.pi*t4))*np.sin(2*np.pi*10*i*t4*fmod_freq_ratio)/10)
		y2=y2*vol/20
		y2=y2*(1+amod_depth*np.sin(2*np.pi*amod_freq*t4))
		done=1
		sound(y2)
		pygame.quit()
		plot.plot(t4,y2)
		plot.show()
	k=0
	prev_k=0
	f0=[]
	f0.append([])
	f0.append([])

	
	while not done:
		clock.tick(5000)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

		keypress = pygame.key.get_pressed()
		if keypress[K_a]:
			f0[k].append(261.63)
		if keypress[K_w]:
			f0[k].append(277.18)
		if keypress[K_s]:
			f0[k].append(293.66)
		if keypress[K_e]:
			f0[k].append(311.13)
		if keypress[K_d]:
			f0[k].append(329.63)
		if keypress[K_f]:
			f0[k].append(349.23)
		if keypress[K_t]:
			f0[k].append(369.99)
		if keypress[K_g]:
			f0[k].append(392.00)
		if keypress[K_y]:
			f0[k].append(415.30)
		if keypress[K_h]:
			f0[k].append(440.00)
		if keypress[K_u]:
			f0[k].append(466.16)
		if keypress[K_j]:
			f0[k].append(493.88) 
		if keypress[K_k]:
			f0[k].append(523.25)
		if keypress[K_o]:
			f0[k].append(554.37) 
		if keypress[K_l]:
			f0[k].append(587.33)
		if keypress[K_p]:
			f0[k].append(622.25)
		if keypress[K_SEMICOLON]:
			f0[k].append(659.25)
		if keypress[K_q]:
			done=True

		if len(f0[k]) !=0 :
			# for initial enter
			if f0[k] != f0[prev_k]:
				p1=[]
				y=0
				y1=0
				if make_variable:
					cutoff=(low_freq+high_freq)/2-(high_freq-low_freq)*np.cos(np.pi*t1)/2
				for i in range(len(f0[k])):
					for j in range(1,harmonics+1):
						f=j*f0[k][i]
						y=y+mod_H(f,cutoff)*a[j]*np.sin(2*np.pi*f*t1+(fmod_depth+fmod_depth_change*np.sin(2*np.pi*t1))*np.sin(2*np.pi*f*t1*fmod_freq_ratio))
						y1=y1+a[j]
				y=y*vol/y1
				y=y*(1+amod_depth*np.sin(2*np.pi*amod_freq*t1))
				phase=t1[int(sample_rate*(attack+dt)-1)]+1/sample_rate
				for i in range(0,int(sample_rate*attack)):
					y[i]=i*y[i]/(sample_rate*attack)
				for i in range(int(sample_rate*attack),int(sample_rate*(attack+dt))):
					y[i]=(1-(1-sh)*(i/sample_rate-attack)/decay)*y[i]
				ht=1-(1-sh)*dt/decay
				for i in range(0,int(sample_rate*(attack+dt))):
					p1.append(y[i])
				sound(y)

			# for sustain
			else:
				x=0
				x1=0
				if make_variable:
					cutoff=(low_freq+high_freq)/2-(high_freq-low_freq)*np.cos(np.pi*(t2+phase))/2
				for i in range(len(f0[k])):
					for j in range(1,harmonics+1):
						f = j*f0[k][i]
						x= x + mod_H(f,cutoff)*a[j]*np.sin(2*np.pi*f*(t2+phase) + (fmod_depth+fmod_depth_change*np.sin(2*np.pi*(t2+phase)))*np.sin(2*np.pi*f*(t2+phase)*fmod_freq_ratio))
						x1=x1+a[j]
				x=x*vol/x1
				x=x*(1+amod_depth*np.sin(2*np.pi*amod_freq*(t2+phase)))
				phase=phase+t2[int(sample_rate*dt-1)]+1/sample_rate

				if ht> sh :
					for i in range(0,int(sample_rate*dt)):
						x[i]=(ht-(1-sh)*(i/sample_rate)/decay)*x[i]
					ht=ht-(1-sh)*dt/decay
				else: x=sh*x 
				for i in range(0,int(sample_rate*dt)):
					p1.append(x[i])
				sound(x)
		#for releasing
		elif f0[k] != f0[prev_k] :
			z=0
			z1=0
			if make_variable:
					cutoff=(low_freq+high_freq)/2-(high_freq-low_freq)*np.cos(np.pi*(t3+phase))/2
			for i in range(len(f0[prev_k])):
				for j in range(1,harmonics+1):
					f=j*(f0[prev_k][i])
					z=z+mod_H(f,cutoff)*a[j]*np.sin(2*np.pi*f*(t3+phase)+(fmod_depth+fmod_depth_change*np.sin(2*np.pi*(t3+phase)))*np.sin(2*np.pi*f*(t3+phase)*fmod_freq_ratio))
					z1=z1+a[j]
			z=z*vol/z1
			z=z*(1+amod_depth*np.sin(2*np.pi*amod_freq*(t3+phase)))
			phase=0
			for i in range(0,int(sample_rate*(release))):
				z[i]=(-1)*ht*(i/sample_rate-release)*z[i]/release
				p1.append(z[i])
			sound(z)
			t=[]
			for i in range(0,len(p1)):
				t.append(i/sample_rate)
			#plot.plot(t,p1)				#just remove hashtag(in both line) if you want to see the waveform
			#plot.show()				
		
		while len(f0[prev_k]) > 0 : f0[prev_k].pop()
		prev_k=k
		if k==0: k=1
		else: k=0

	stream.stop_stream()
	stream.close()
	p.terminate()
	pygame.quit()
	
def makeform(root):

	entries = []
	
	#first line
	row =Frame(root)
	row.config(bg='light green')
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, bg='light green',font = "Times",text='WAVEFORMS  ', anchor='e')
	lab.pack(side=LEFT)
	lab = Label(row, width=50, bg='light green',font = "Times",text='ADSR ENVELOPE  ', anchor='e')
	lab.pack(side=LEFT)

	#2nd line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, text='No.of Harmonics  ', anchor='e')
	lab.pack(side=LEFT)
	harmonics=Entry(row)
	harmonics.config(width=3)
	harmonics.pack(side=LEFT)

	lab = Label(row, width=50, text='Attack time(in msec)  ', anchor='e')
	lab.pack(side=LEFT)
	attack=Entry(row)
	attack.config(width=5)
	attack.pack(side=LEFT)

	#3rd line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, text='Square wave ', anchor='e')
	lab.pack(side=LEFT)
	square = IntVar()
	lab = Checkbutton(row, variable=square)
	lab.pack(side=LEFT) 

	lab = Label(row, padx=3,width=50, text='Decay time(in msec)  ', anchor='e')
	lab.pack(side=LEFT)
	decay=Entry(row)
	decay.config(width=5)
	decay.pack(side=LEFT)

	#4th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Triangle wave ', anchor='e')
	lab.pack(side=LEFT)
	triangle = IntVar()
	lab = Checkbutton(row, variable=triangle)
	lab.pack(side=LEFT) 

	lab = Label(row, width=45, text='Sustain level :', anchor='e')
	lab.pack(side=LEFT)

	#5th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Sawtooth wave ', anchor='e')
	lab.pack(side=LEFT)
	sawtooth = IntVar()
	lab = Checkbutton(row, variable=sawtooth)
	lab.pack(side=LEFT) 

	sustain =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=-30, to=0)
	sustain.set(0)
	sustain.pack( side=LEFT,padx=210)

	#6th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, text='Noise ', anchor='e')
	lab.pack(side=LEFT)
	noise = IntVar()
	lab = Checkbutton(row, variable=noise)
	lab.pack(side=LEFT) 

	lab = Label(row, padx=3,width=50, text='Release time(in msec)  ', anchor='e')
	lab.pack(side=LEFT)
	release=Entry(row)
	release.config(width=5)
	release.pack(side=LEFT)	

	#7th line
	row =Frame(root)
	row.config(bg='light green')
	row.pack(side=TOP, fill=X, pady=30)
	lab = Label(row, width=55, bg='light green',font = "Times",text='FILTERS AND FREQUENCY EQUALIZATION  ', anchor='e')
	lab.pack(side=LEFT)
	lab = Label(row, width=40, bg='light green',font = "Times",text='FREQUENCY INPUTS  ', anchor='e')
	lab.pack(side=LEFT)

	#8th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, text='Order of Butterworth Filter  ', anchor='e')
	lab.pack(side=LEFT)
	order=Entry(row)
	order.config(width=3)
	order.pack(side=LEFT)

	lab =Label(row,width=50,text='fixed cutoff frequency :',anchor='e')
	lab.pack(side=LEFT)
	fix_cutoff_freq = Entry(row)
	fix_cutoff_freq.config(width=5)
	fix_cutoff_freq.pack(side=LEFT)

	#9th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Lowpass ', anchor='e')
	lab.pack(side=LEFT)
	lowpass= IntVar()
	lab = Checkbutton(row, variable=lowpass)
	lab.pack(side=LEFT) 

	lab =Label(row,padx=3,width=50,text='Band Width :',anchor='e')
	lab.pack(side=LEFT)
	band_width = Entry(row)
	band_width.config(width=5)
	band_width.pack(side=LEFT)

	#10th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Highpass ', anchor='e')
	lab.pack(side=LEFT)
	highpass=IntVar()
	lab = Checkbutton(row, variable=highpass)
	lab.pack(side=LEFT) 

	lab =Label(row,width=50,text='Time varient cutoff frequency',anchor='e')
	lab.pack(side=LEFT)

	#11th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Bandpass ', anchor='e')
	lab.pack(side=LEFT)
	bandpass= IntVar()
	lab = Checkbutton(row, variable=bandpass)
	lab.pack(side=LEFT) 

	lab=Label(row, padx=3,width=50, text='lower frequency : ', anchor='e')
	lab.pack(side=LEFT)
	low_freq = Entry(row)
	low_freq.config(width=5)
	low_freq.pack(side=LEFT)

	#12th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)	
	lab = Label(row, width=40, text='Volume at equalizing frequency : ', anchor='e')
	lab.pack(side=LEFT)

	lab=Label(row,padx=4, width=53, text='higher frequency : ', anchor='e')
	lab.pack(side=LEFT)
	high_freq = Entry(row)
	high_freq.config(width=5)
	high_freq.pack(side=LEFT)

	#13th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	vol_equilizer =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=-20, to=20)
	vol_equilizer.set(0)
	vol_equilizer.pack(side=LEFT, padx=125)

	#14th line
	row =Frame(root)
	row.config(bg='light green')
	row.pack(side=TOP, fill=X, pady=30)
	lab = Label(row, width=40, bg='light green',font = "Times",text='AMPLITUDE MODULATION  ', anchor='e')
	lab.pack(side=LEFT)
	lab = Label(row, width=55, bg='light green',font = "Times",text='FREQUENCY MODULATION  ', anchor='e')
	lab.pack(side=LEFT)

	#15th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab = Label(row, width=40, text='AM frequency : ', anchor='e')
	lab.pack(side=LEFT)
	amod_freq = Entry(row)
	amod_freq.config(width=5)
	amod_freq.pack(side=LEFT)

	lab = Label(row, width=50, text='FM frequency ratio :-   1: ', anchor='e')
	lab.pack(side=LEFT)
	fmod_freq = Entry(row)
	fmod_freq.config(width=3)
	fmod_freq.pack(side=LEFT)

	#16th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab =Label(row,width=30,text='AM depth :',anchor='e')
	lab.pack(side=LEFT)

	lab =Label(row,width=55,text='FM depth :',anchor='e')
	lab.pack(side=LEFT)

	#17th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	amod_depth =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=-30, to=0)
	amod_depth.set(-20)
	amod_depth.pack(side=LEFT,padx=125)

	fmod_depth =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=0, to=50)
	fmod_depth.set(20)
	fmod_depth.pack(side=LEFT, padx=70)

	#18th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	lab =Label(row,width=30,text='Volume :',anchor='e')
	lab.pack(side=LEFT)

	lab =Label(row,width=60,text='FM depth Variation :',anchor='e')
	lab.pack(side=LEFT)

	#19th line
	row =Frame(root)
	row.pack(side=TOP, fill=X)
	volume =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=-30, to=0)
	volume.set(-6)
	volume.pack(side=LEFT,padx=125)
	
	fmod_depth_change =Scale(row, orient=HORIZONTAL,length=240, sliderlength=10, from_=0, to=100)
	fmod_depth_change.set(0)
	fmod_depth_change.pack(side=LEFT, padx=70)


	entries.append(harmonics)
	entries.append(attack)
	entries.append(decay)
	entries.append(release)
	entries.append(square)
	entries.append(triangle)
	entries.append(sawtooth)
	entries.append(order)
	entries.append(lowpass)
	entries.append(highpass)
	entries.append(bandpass)
	entries.append(band_width)
	entries.append(vol_equilizer)
	entries.append(sustain)
	entries.append(volume)
	entries.append(fix_cutoff_freq)
	entries.append(amod_freq)
	entries.append(amod_depth)
	entries.append(fmod_freq)
	entries.append(fmod_depth)
	entries.append(low_freq)
	entries.append(high_freq)
	entries.append(fmod_depth_change)
	entries.append(noise)

	return entries

if __name__ == '__main__':
	root = Tk()
	root.title('Music synthesizer')
	ents = makeform(root) 
	
	root.bind('<Return>', (lambda event,e=ents: fetch(e)))   
	b1 = Button(root, text='Go',
		     command=(lambda e=ents: fetch(e)))
	b1.pack(side=LEFT, padx=5, pady=5)
	b2 = Button(root, text='Quit', command=root.quit)
	b2.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()
