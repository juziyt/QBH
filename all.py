import tkSnack, Tkinter
import line
import os, wave
import audioop as Audio


class ConstructTags(tkSnack.Sound):
    def __init__(self, Song=None):
        tkSnack.Sound.__init__(self,load=Song)
        self.Length = None
        self.sampling_rate = None
#        self.Stream = None
        self.FragmentFactor = 256
        self.ByteLength = None

    def load(self,Song):
        self.read(Song)
#        self.configure(channels=1, fileformat='WAV')#, encoding='Lin8')#, frequency=44100)
        self.ByteLength = 1
        self.Length = self.length(unit="SAMPLES")
        self.sampling_rate = self.cget("frequency")
#        Temp = wave.open(".temp.wav","rb")
#        self.Stream = Temp.readframes(self.Length)
#        Temp.close()
#        os.remove(".temp.wav")

    def get_minmax_tag(self):
        min_list = []
        max_list = []
        self.write(".temp.wav")
        Song = wave.open(".temp.wav","rb")
        NumStream = Song.getnframes()
        BufferLen = NumStream / self.FragmentFactor
        Stream = Song.readframes(BufferLen)
        while len(Stream):
            Stream = Audio.lin2lin(Stream,2,1)
            Stream = Audio.tomono(Stream,1,1,-1)
            min_val, max_val = Audio.minmax(Stream, self.ByteLength)
            min_list.append(min_val)
            max_list.append(max_val)
            Stream = Song.readframes(BufferLen)
        Song.close()
        os.remove(".temp.wav")
        return min_list, max_list

    def get_tags(self):
        spectrum = self.dBPowerSpectrum()
        slope = line.normalize(spectrum)
        min_list, max_list = self.get_minmax_tag()
        return (slope, max_list, min_list)

def main(path):
    Tags=[]
    root = Tkinter.Tk()
    tkSnack.initializeSnack(root)
    Song = ConstructTags()
    for Song_Name in os.listdir(path):
        Song_Path = path+Song_Name
        Song.load(Song_Path)
        Slope, max_list, min_list = Song.get_tags()
        Tags.append({"Name":Song_Name, "Path":Song_Path, "Slope":Slope, "MaxList":max_list, "MinList":min_list})

#    print len(Tags)
    del(root)
    return Tags
