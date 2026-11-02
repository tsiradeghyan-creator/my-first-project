-I- 1
size 1280 536
fps 24
letterbox 720

shot 5.5 "Տիգրանը խոսում է"
  actor king ../storyboard/panels/10.png
  king idle
  king say "Մենք չենք նահանջում։ Մենք կվերադառնանք։" at 0.5 pitch 22 speed 120
  king look -0.04 from 3.6 to 5.5 fade 0.6
  camera push 1.05

shot 5.0 "Սուրհանդակը քայլում է"
  actor m ../storyboard/refs/REF_E_king_full_hall.png
  m idle
  m walk speed 0.8 from 0.3 to 4.8 fade 0.35
  camera pan -30 0

shot 4.0 "Թագավորը գալիս է"
  actor king ../storyboard/panels/09.png
  king walk speed 0.9 from 0.0 to 4.0 fade 0.3
  camera push 1.03

