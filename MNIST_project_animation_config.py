
def set_config(c):
    c.input_path = "workspaces/MNIST_workspace/data/MNIST_animation.npz"
    c.compression_ratio = 50
    c.epochs = 100
    c.batch_size = 128
    c.lr = 0.001
    c.model_name = "AE"
    c.model_type = "dense"
    c.data_dimension = 2
    c.early_stopping = True
    c.early_stopping_patience = 10
    c.min_delta = 0.001
    c.lr_scheduler = True
    c.lr_scheduler_patience = 5
    c.custom_norm = False
    c.l1 = False
    c.reg_param = 0.0001
    c.apply_normalization = True
    c.test_size = 0.1
    c.deterministic_algorithm = True
    c.activation_extraction = False
    c.compress_to_latent_space = True
    c.save_error_bounded_deltas = False
    c.convert_to_blocks = False
    c.intermittent_model_saving = True
    c.intermittent_saving_patience = 10
