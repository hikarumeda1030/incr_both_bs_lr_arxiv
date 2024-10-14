# INCREASING BOTH BATCH SIZE AND LEARNING RATE ACCELERATES STOCHASTIC GRADIENT DESCENT
Source code for reproducing our paper's experiments.

The results of the experiments can be found in the [Result Directory](./result/README.md).
# Abstract
The performance of mini-batch stochastic gradient descent (SGD) strongly depends on setting the batch size and learning rate to minimize the empirical loss in training the deep neural network. In this paper, we present theoretical analyses of mini-batch SGD with four schedulers: (i) constant batch size and decaying learning rate scheduler, (ii) increasing batch size and decaying learning rate scheduler, (iii) increasing batch size and increasing learning rate scheduler, and (iv) increasing batch size and warm-up decaying learning rate scheduler. We show that mini-batch SGD using scheduler (i) does not always minimize the expectation of the full gradient norm of the empirical loss, whereas it does using any of schedulers (ii), (iii), and (iv). Furthermore, schedulers (iii) and (iv) accelerate mini-batch SGD. The paper also provides numerical results of supporting analyses showing that using scheduler (iii) or (iv) minimizes the full gradient norm of the empirical loss faster than using scheduler (i) or (ii).

# Usage

To train a model on **CIFAR-100**, run `cifar100.py` with a JSON file specifying the training parameters. Optionally, use the `--cuda_device` argument to choose a CUDA device. The default is device `0`:

```bash
python cifar100.py XXXXX.json --cuda_device 1
```

To resume training from a checkpoint, add the `--resume` option to the command. This will load the model state from the checkpoint specified in `checkpoint_path` within the JSON file and continue training from that point:

```bash
python cifar100.py XXXXX.json --resume --cuda_device 1
```

For more details about configuring checkpoints, refer to the `checkpoint_path` section in the **Parameters Description**.

### Customizing Training

To customize the training process, modify the parameters in the JSON file and rerun the script. You can adjust the model architecture, learning rate, batch size, and other parameters to explore different training schedulers and observe their effects on model performance.

### Training on CIFAR10 and Tiny ImageNet

To train a model on **CIFAR10** or **Tiny ImageNet**, use the respective scripts `cifar10.py` or `tiny_imagenet.py`. The method for both is similar, as shown below:

For **CIFAR10**:
```bash
python cifar10.py XXXXX.json --cuda_device 1
python cifar10.py XXXXX.json --resume --cuda_device 1
```

For **Tiny ImageNet**:
```bash
python tiny_imagenet.py XXXXX.json --cuda_device 1
python tiny_imagenet.py XXXXX.json --resume --cuda_device 1
```

## Example JSON Configuration
The following JSON configuration file is located at `src/json/incr_bs_warmup_lr/warmup_const_lr_max0.2.json`:
```
{
    "model": "resnet18",
    "bs_method": "exp_growth",
    "lr_method": "warmup_const",
    "init_bs": 8,
    "init_lr": 0.1,
    "lr_max": 0.2,
    "epochs": 300,
    "incr_interval": 30,
    "warmup_epochs":30,
    "warmup_interval":3,
    "bs_growth_rate": 2.0,
    "checkpoint_path": "checkpoint/warmup_const_lr_max0.2.pth.tar",
    "csv_path": "../result/incr_bs_warmup_lr/warmup_const_lr_max0.2/"
}
```
### Parameters Description
| Parameter | Value | Description |
| :-------- | :---- | :---------- |
| `model` | `"resnet18"`, `"WideResNet28_10"`, etc. | Specifies the model architecture to use. |
| `bs_method` | `"constant"`, `"exp_growth"` | Method for adjusting the batch size. |
|`lr_method`|`"constant"`, `"cosine"`, `"diminishing"`, `"linear"`, `"poly"`, <br>`"exp_growth"`,<br>`"warmup_const"`, `"warmup_cosine"`|Method for adjusting the learning rate.|
|`init_bs`|`int` (e.g., `128`)| The initial batch size for the optimizer. |
|`bs_max`|`int` (e.g., `4096`)| The maximum batch size to be reached when increasing the batch size, if an upper limit is desired. Used when `bs_method` is `"exp_growth"`.|
|`init_lr`|`float` (e.g., `0.1`)| The initial learning rate for the optimizer. |
|`lr_max`|`float` (e.g., `0.2`)|The maximum learning rate to be reached when increasing the learning rate, if an upper limit is desired. Used when `lr_method` is `"exp_growth"`, `"warmup_const"`, or `"warmup_cosine"`.|
|`lr_min`|`float` (e.g., `0.001`)| The minimum learning rate to be used in the cosine annealing schedule. Used when `lr_method` is `"cosine"` or `"warmup_cosine"`. The default value is `0`.|
|`epochs`|`int` (e.g., `300`)|The total number of epochs for training.|
|`incr_interval`|`int` (e.g., `30`)|Interval (in epochs) at which the batch size will increase. Also, the interval for increasing the learning rate when `lr_method` is `"exp_growth"`. Used when `bs_method` is `"exp_growth"`.|
|`warmup_epochs`|`int` (e.g., `30`)|Number of epochs over which the learning rate warms up from `init_lr` to `lr_max`. Used when `lr_method` is `"warmup_const"` or `"warmup_cosine"`.|
|`warmup_interval`|`int` (e.g., `3`)|The interval (in epochs) during which the learning rate increases in the warmup phase. Used when `lr_method` is `"warmup_const"` or `"warmup_cosine"`.|
|`bs_growth_rate`|`float` (e.g., `2.0`)|The factor by which the batch size increases after each interval. Used when `bs_method` is `"exp_growth"`.|
|`lr_growth_rate`| `float` (e.g., `1.4`) |The factor by which the learning rate increases after each interval. Used when `lr_method` is `"exp_growth"`, `"warnup_const`", or `"warmup_cosine"`.|
|`power`| `float` (e.g., `2.0`) |A parameter used when `lr_method` is set to `"poly"`, defining the polynomial decay rate of the learning rate.|
|`checkpoint_path`|`str` (e.g., `"checkpoint/XXXXX.pth.tar"`)|Specifies any `"pth.tar"` file in the `checkpoint` directory. Checkpoints are saved at each epoch. If `--resume` is added to the command (`python cifar100.py json/XXXXX.json --resume`), training can be resumed from the checkpoint.|
|`csv_path`|`str` (e.g., `"path/to/result/csv/"`)|Specifies the directory where CSV files will be saved. Four CSV files—`train.csv`, `test.csv`, `norm.csv`, and `lr_bs.csv`—will be saved in this directory.|
