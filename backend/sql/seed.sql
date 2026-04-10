INSERT INTO places (name, latitude, longitude, address, hashtag, wifi, indoor, outdoor)
VALUES
  ('JP Park', 12.9037, 77.5857, 'JP Nagar, Bengaluru', '#park #quiet', true, false, true),
  ('Corner Hub Cafe', 12.9088, 77.5834, 'JP Nagar 6th Phase, Bengaluru', '#cafe #wifi', true, true, false),
  ('Bahubali Library', 12.9061, 77.5799, 'Banashankari, Bengaluru', '#library #focus', true, true, false),
  ('Study Nest CoWork', 12.9152, 77.5938, 'Jayanagar 4th Block, Bengaluru', '#cowork #students', true, true, false),
  ('Silent Square', 12.9113, 77.6015, 'BTM Layout, Bengaluru', '#indoor #calm', true, true, false),
  ('Green Bench Spot', 12.8981, 77.6004, 'Puttenahalli, Bengaluru', '#outdoor #green', false, false, true),
  ('Night Owl Reading Room', 12.9212, 77.5871, 'Jayanagar 9th Block, Bengaluru', '#late-night #library', true, true, false),
  ('Campus Brew Corner', 12.9264, 77.5928, 'Near South End Circle, Bengaluru', '#coffee #group-study', true, true, false)
ON CONFLICT (name) DO NOTHING;
