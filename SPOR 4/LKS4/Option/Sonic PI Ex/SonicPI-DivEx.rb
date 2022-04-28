# eksempler fra
# https://www.youtube.com/watch?v=4BPKaHV7Q5U&list=PLaitaNxyd8SHvTQjRGnMdKLsARXW7iYyp&index=2

use_synth_defaults attack: 0, decay: 0, sustain_level: 1, sustain: 0, release: 0.1

loop do
  play (ring 60,64,67,72,76).tick  #choose
  sleep 1
end

#loop do
#  play (scale :c2, :major_pentatonic, num_octaves: 4).tick
#  sleep 0.25
#end

use_synth :tb303
#loop do
#  play (scale :c2, :minor_pentatonic, num_octaves: 2).choose
#  sleep 0.25
#end

#loop do
#  play (chord :c3, '13').choose
#  sleep 0.25
#end

#notes = (scale :e3, :minor_pentatonic, num_octaves: 2).shuffle
#s = play 60
#sleep 3
#27.times do
#  control s, note: notes.tick
#  sleep 0.5
#end

#s = sample :ambi_lunar_land
#pan_ring = (ring -1,1)
#10.times do
#  control s, pan: pan_ring.tick
#  sleep 0.5
#end

#live_loop :mybeat do
#  8.times do
#    sample :bd_pure
#    sleep 0.5
#  end
#end

#live_loop :mysample do
#  sync :mybeat
#  sample :ambi_piano
#end



