# Sonic PI drumbeat6.rb  (simple version wo global variables
# Drum beat in grid - inspired from: https://www.youtube.com/watch?v=RaJZho7p2Y4
# Version 0.6 13 april 2021 Knud Funch, SoundHub Denmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Music intro: https://learningmusic.ableton.com/make-beats/make-beats.html
# Added control from OSC - making paterns and sample setting global
# Added loops to receive controls and paterns via OSC
#
# Define patern etc. as globals so it can be manipulated from elsewhere:
# Default patern given that mathces page 2 in "learning music from ableton"
#
# Further improvement could be to make more than one bar to make more variation possible
#
# Pos i bar     1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
# Idx           0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
# Beat          1           2           3           4
# Sub           1  2  3  4  1  2  3  4  1  2  3  4  1  2  3  4
open_p    =    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
closed_p  =    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
snare_p   =    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
kick_p    =    [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0]

# Set default samples
open_s   = :drum_cymbal_open
closed_s = :drum_cymbal_closed
snare_s  = :sn_zome
kick_s   = :drum_heavy_kick

# default and control variables to be changed via OSC
tempo = 60
drumbeat_on = true

live_loop :drumbeat do
  use_bpm tempo
  if drumbeat_on then
    16.times do |i|
      sample open_s   if open_p[i]   == 1
      sample closed_s if closed_p[i] == 1
      sample snare_s  if snare_p[i]  == 1
      sample kick_s   if kick_p[i]   == 1
      if not drumbeat_on then
        break   # stop before ending bar when drumbeat is set to off from outside
      end
      sleep 0.25  # 4 times per beat
    end
  else
    sleep 0.25
  end
end


live_loop :drumbeat_control do
  use_real_time
  t,v = sync "/osc*/trigger/drumbeat_control"
  tempo = v if t == "tempo"
  if t == "on_off" then
    drumbeat_on = true  if v == 1
    drumbeat_on = false if v == 0
  end
end

live_loop :drumbeat_patern_open do
  use_real_time
  open_p = sync "/osc*/trigger/drumbeat_patern_open"
end

live_loop :drumbeat_patern_closed do
  use_real_time
  closed_p = sync "/osc*/trigger/drumbeat_patern_closed"
end

live_loop :drumbeat_patern_snare do
  use_real_time
  snare_p = sync "/osc*/trigger/drumbeat_patern_snare"
end

live_loop :drumbeat_patern_kick do
  use_real_time
  kick_p = sync "/osc*/trigger/drumbeat_patern_kick"
end

live_loop :drumbeat_set_sample do
  use_real_time
  t,s = sync "/osc*/trigger/drumbeat_set_sample"
  open_s   = s if t == "open"
  closed_s = s if t == "closed"
  snare_s  = s if t == "snare"
  kick_s   = s if t == "kick"
end



