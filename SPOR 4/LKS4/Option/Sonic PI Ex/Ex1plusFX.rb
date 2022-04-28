# Welcome to Sonic Pi v3.1
# Ex1PlusFX.rb
live_loop :foo1 do
  use_real_time
  s, n, a, p = sync "/osc*/trigger/synth"
  use_synth s
  with_fx :reverb, room: 1 do
    play hz_to_midi(n), amp: a, pan: p, release: 0.8, attack: 0.2
    # evt lav release og attack til parametre som overføres...
    # og måske størrelsen på room
    # og måske ovenikøbet selve FX ...
    # det hele kan komme over ... men vælg med omhu :-)
  end
end

live_loop :foo2 do
  use_real_time
  s, n, a, p, ps = sync "/osc*/trigger/sample"
  with_fx :echo do
    sample s, rate: n, amp: a, pan: p, pitch: ps, window_size: 0.5
  end
end
