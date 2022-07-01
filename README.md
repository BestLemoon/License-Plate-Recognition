# License-Plate-Recognition
Licenses plate detection and recognition with yolox

## Train

```shell
pip install -r requirements.txt
```

- Place your own dataset in the data folder with data.yml

- Run Train with this command

  ```bash
  python3 train.py 
  --img 736 
  --batch 16 
  --epochs 32 
  --data /path/to/data.yml 
  --weights /path/to/weight.pt 
  --cache
  ```

## Dataset

You can process your own CCPD datasets with the script in  `pre_process`

- `CCPD2YOLO`:Transform the CCPD images name into YoLov5txt format and auto generate data.yml
- `RandomSample`: Select a mount of sample images from your original datasets.

## Predict

You are supposed to modify the parameters in the `detect_one_with_wrap.py` or `detect_batch.py`if you want to predict some images in one batch.

# Text Recognition

## PaddleOCR

We have chosen [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) to recognize the text in the license plate. The steps are as follow.

> You are supposed to download the pretrained model in the `.\pretrain_models` folder.

## Model Trainning

```shell
python3 tools/train.py 
-c configs/rec/ch_PP-OCRv2/ch_PP-OCRv2_rec.yml 
-o Global.pretrained_model=pretrained_model/ch_PP-OCRv2_rec_train/best_accuracy
```

## Infer

```
python3 yolov5/run.py
```

> We created the interface using pyqt5 and modified predict_rec.py and utility.py in the reg/PaddleOCR/tools/infer folder. If you need to execute commands in the terminal, download the original code from the PaddleOCR official website and execute:
> python3 tools/infer/predict_rec.py 

## References

- GitHub. 2022. *GitHub - xialuxi/yolov5-car-plate: 基于yolov5的车牌检测，包含车牌角点检测*. [online] Available at: <https://github.com/xialuxi/yolov5-car-plate> [Accessed 8 June 2022].
- **[ SIoU Loss: More Powerful Learning for Bounding Box Regression](https://arxiv.org/abs/2205.12740) [cs.CV]**
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

