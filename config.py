def update_folder(config, folder):
    import os
    config.log_path = os.path.join(config.log_path, folder)
    config.sample_path = os.path.join(config.sample_path, folder)
    config.model_save_path = os.path.join(config.model_save_path, folder)


def remove_folder(config):
    import os
    samples = os.path.join(config.sample_path, '*.jpg')
    samples_txt = os.path.join(config.sample_path, '*.txt')
    models = os.path.join(config.model_save_path, '*.pth')
    print("YOU ARE ABOUT TO REMOVE EVERYTHING IN:\n{}\n{}\n{}".format(
        samples, samples_txt, models))
    input("ARE YOU SURE?")
    os.system("rm {} {} {}".format(samples, samples_txt, models))


def UPDATE_FOLDER(config, str):
    if getattr(config, str):
        update_folder(config, str)


def update_config(config):
    import os
    import glob

    update_folder(config, config.dataset_fake)
    if '/' in config.dataset_fake:
        config.dataset_fake = config.dataset_fake.split('/')[0]
    config.batch_size *= 2  # RaGAN
    config.num_epochs *= config.save_epoch
    config.num_epochs_decay *= config.save_epoch

    if config.image_size != 256:
        update_folder(config, 'image_size_' + str(config.image_size))

    if config.DELETE:
        remove_folder(config)

    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)
    if not os.path.exists(config.model_save_path):
        os.makedirs(config.model_save_path)
    if not os.path.exists(config.sample_path):
        os.makedirs(config.sample_path)

    if config.pretrained_model is None:
        try:
            config.pretrained_model = sorted(
                glob.glob(os.path.join(config.model_save_path, '*_G.pth')))[-1]
            config.pretrained_model = '_'.join(
                os.path.basename(config.pretrained_model).split('_')[:-1])
        except BaseException:
            pass

    if config.mode == 'train':
        config.loss_plot = os.path.abspath(
            os.path.join(config.sample_path, 'loss.txt'))
        config.log = os.path.abspath(
            os.path.join(config.sample_path, 'log.txt'))
        of = 'a' if os.path.isfile(config.log) else 'w'
        config.log = open(config.log, of)
        os.system('touch ' + config.log.name)

    return config
