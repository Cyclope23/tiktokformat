# TikTok didattica

Percorso episodio: episodi/classe-N/NN-argomento-linguaggio/
Dentro: .mp4 (video), .txt (descrizione, richiamo teorico, hashtag), .json (sorgente).
Regole: minuscolo, trattini, numero progressivo per classe.
Rigenerare un episodio: python3 strumenti/render.py <file.json> -o <file.mp4> [--music brano.mp3] [--set cps=22]
(richiede ffmpeg, g++, Pillow, Pygments)
