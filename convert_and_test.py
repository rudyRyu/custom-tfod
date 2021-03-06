import glob
import os

from model_utils.export_tflite_graph import export_tflite_graph

from convert_tflite.main import convert_tflite_int8
from train.input_pipeline import generate_tfdataset

from inference.inference_tflite import InferenceModel, image_inference

# 0. configure
model_name = 'LPD_mobilenet_v2_keras_pretrained_dropout'
checkpoint_name = 'best-96'

saved_model_path = f'./checkpoints/{model_name}/saved_model/'
img_size_hw = [320,320]
dataset = 'data/test.tfrecord'
quant_level = 2
tflite_path = 'lpd_mobilenet_v2_keras_pretrained_dropout_320.tflite' #f'./tflite_models/{model_name}_{checkpoint_name}.tflite'

test_image_dir = 'inference/test_images/lp'
result_image_dir = 'inference/result_images/lp'


# 1.create saved model
meta_info_path = f'./checkpoints/{model_name}'
export_tflite_graph(meta_info_path+'/meta_info.config', meta_info_path,
                    checkpoint_name=checkpoint_name)


# 2. convert to tflite
dataset = generate_tfdataset(dataset, 1, img_size_hw)
convert_tflite_int8(saved_model_path, dataset, tflite_path, quant_level)


# 3. test images with tflite
exts = ['*.jpg', '*.jpeg', '*.png']
img_paths = []
for ext in exts:
    img_paths.extend(glob.glob(os.path.join(test_image_dir, ext)))
os.makedirs(result_image_dir, exist_ok=True)

img_paths.sort()
model = InferenceModel(tflite_path)
for img_path in img_paths:
    img_name = os.path.basename(img_path)
    image_inference(model, img_path, os.path.join(result_image_dir, img_name))
