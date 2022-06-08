# License-Plate-Recognition
Licenses plate detection and recognition with yolox

## Train

- ```shell
	pip install -r requirements.txt
	```

- Place your own dataset in the data folder with data.yml

- Run Train with this command

	```bash
	python train.py --img 736 --batch 16 --epochs 32 --data /path/to/data.yml --weights /path/to/weight.pt --cache
	```

## Dataset

You can process your own CCPD datasets with the script in  `pre_process`

- `CCPD2YOLO`:Transform the CCPD images name into YoLov5txt format and auto generate data.yml
- `RandomSample`: Select a mount of sample images from your original datasets.

## Predict

You are supposed to modify the parameters in the `detect_one_with_wrap.py` or `detect_batch.py`if you want to predict some images in one batch.

## References

- GitHub. 2022. *GitHub - xialuxi/yolov5-car-plate: 基于yolov5的车牌检测，包含车牌角点检测*. [online] Available at: <https://github.com/xialuxi/yolov5-car-plate> [Accessed 8 June 2022].

- **[ SIoU Loss: More Powerful Learning for Bounding Box Regression](https://arxiv.org/abs/2205.12740) [cs.CV]**

