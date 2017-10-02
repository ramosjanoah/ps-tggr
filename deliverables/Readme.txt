Src: folder yang berisi source semua pos tagger dengan semua model.
	pos-tagger-3model.py berarti untuk model tree, KNN, dan Naive Bayes
	pos-tagger-crf.py berarti untuk model CRF
	Pastikan anda memiliki package berikut untuk menjalankannya:
		- sklearn
		- sklearn-crfsuite
		- conllu

Bin: folder untuk menjalankan pos tagging. Menggunakan algoritma CRF.
	Ubah kalimat pada input.txt untuk mengubah kalimat yang ingin diklasifikasi.
	Pastikan anda memiliki package berikut untuk menjalankannya:
		- sklearn-crfsuite
		- conllu