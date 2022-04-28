# Welcome to Sonic Pi v3.1
# Klokke.rb
# loop med klokker giver et klokke spil med random funktion og pitch change
# Forudsætter fil og sti er korrekt!!
sample "C:/Lyde/Ding-1sek.wav"
sleep 3
loop do
  sample "C:/Lyde/Ding-1sek.wav", rate: rrand(0.02,1.3), pan: rrand(-1,1)
  sleep 1
end