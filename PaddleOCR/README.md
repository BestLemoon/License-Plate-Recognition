# Text Recognition

## PaddleOCR

We have chosen [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) to recognize the text in the license plate. The steps are as follow.

> You are supposed to download the pretrained model in the `.\pretrain_models` folder.

## Model Trainning

```shell
python3 tools/train.py -c configs/rec/ch_PP-OCRv2/ch_PP-OCRv2_rec.yml -o Global.pretrained_model=pretrained_model/ch_PP-OCRv2_rec_train/best_accuracy
```

## Infer



