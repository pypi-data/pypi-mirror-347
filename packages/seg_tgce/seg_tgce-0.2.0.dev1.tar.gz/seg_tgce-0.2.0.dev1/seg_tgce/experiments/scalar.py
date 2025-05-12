import keras_tuner as kt
from keras.models import Model
from keras.optimizers import Adam

from seg_tgce.data.oxford_pet.oxford_pet import (
    fetch_models,
    get_data_multiple_annotators,
)
from seg_tgce.loss.tgce import TcgeSs
from seg_tgce.metrics import DiceCoefficient, JaccardCoefficient
from seg_tgce.models.unet import unet_tgce_scalar

if __name__ == "__main__":
    TARGET_SHAPE = (128, 128)
    BATCH_SIZE = 8
    NUM_CLASSES = 3
    NUM_SCORERS = 2

    learning_rate = 1e-3
    optimizer = Adam(learning_rate=learning_rate)

    loss_fn = TcgeSs(
        num_classes=NUM_CLASSES,
        q=0.5,
        noise_tolerance=0.5,
        reliability_type="scalar",
        name="TGCE",
    )

    dice_fn = DiceCoefficient(num_classes=NUM_CLASSES)
    jaccard_fn = JaccardCoefficient(num_classes=NUM_CLASSES)

    model = unet_tgce_scalar(
        input_shape=TARGET_SHAPE + (3,),
        n_classes=NUM_CLASSES,
        n_scorers=NUM_SCORERS,
        name="Unet-TGCE-Scalar-Model",
    )

    model.compile(
        metrics=[dice_fn],
        optimizer=optimizer,
    )
    model.loss_function = loss_fn

    noise_levels = [-20.0, 10.0]
    disturbance_models = fetch_models(noise_levels)
    train, val, test = get_data_multiple_annotators(
        annotation_models=disturbance_models,
        target_shape=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
    )

    history = model.fit(
        train,
        epochs=50,
        validation_data=val,
    )

    test_results = model.evaluate(test)
    print(f"Test results: {test_results}")

""" if __name__ == "__main__":
    TARGET_SHAPE = (128, 128)
    BATCH_SIZE = 8
    NUM_CLASSES = 3
    NUM_SCORERS = 2

    def model_builder(hp) -> Model:
        learning_rate = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")
        optimizer = Adam(learning_rate=learning_rate)

        loss_fn = TcgeSs(
            num_classes=NUM_CLASSES,
            q=hp.Float("q", min_value=0, max_value=1),
            noise_tolerance=hp.Float("C", min_value=0, max_value=1),
            reliability_type="scalar",
            name="TGCE",
        )

        dice_fn = DiceCoefficient(num_classes=NUM_CLASSES)
        jaccard_fn = JaccardCoefficient(num_classes=NUM_CLASSES)

        model = unet_tgce_scalar(
            input_shape=TARGET_SHAPE + (3,),
            n_classes=NUM_CLASSES,
            n_scorers=NUM_SCORERS,
            name="Unet-TGCE-Scalar-Model",
        )

        model.compile(
            metrics=[dice_fn],
            optimizer=optimizer,
        )
        model.loss_function = loss_fn
        return model

    tuner = kt.BayesianOptimization(
        model_builder,
        objective=kt.Objective("val_DiceCoefficient", direction="max"),
        directory="results",
        project_name="best_scalar",
    )

    noise_levels = [-20.0, 10.0]
    disturbance_models = fetch_models(noise_levels)
    train, val, test = get_data_multiple_annotators(
        annotation_models=disturbance_models,
        target_shape=TARGET_SHAPE,
        batch_size=BATCH_SIZE,
    )

    tuner.search(
        train.take(12),
        epochs=10,
        validation_data=val.take(6),
    )

    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    print(f"Best hyperparameters: {best_hps.values}")

    best_model = tuner.hypermodel.build(best_hps)
    history = best_model.fit(
        train,
        epochs=50,
        validation_data=val,
    )

    test_results = best_model.evaluate(test)
    print(f"Test results: {test_results}")
 """
