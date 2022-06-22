预训练模型下载：https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_rec_train.tar

模型训练：python tools/train.py 

-c configs/rec/ch_PP-OCRv2/ch_PP-OCRv2_rec.yml 

-o Global.pretrained_model=pretrained_model/ch_PP-OCRv2_rec_train/best_accuracy