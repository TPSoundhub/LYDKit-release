# Ex1
# Modpart til LKS4-simple-7Key-KBOSC.py
live_loop :foo1 do
  use_real_time
  s, n, a, p = sync "/osc*/trigger/synth"
  use_synth s
  play hz_to_midi(n), amp: a, pan: p
end
live_loop :foo2 do
  use_real_time
  s, n, a, p, ps = sync "/osc*/trigger/sample"
  sample s, rate: n, amp: a, pan: p, pitch: ps, window_size: 0.5
end
