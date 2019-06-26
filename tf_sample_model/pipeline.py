from tfx.components.evaluator.component import Evaluator
from tfx.components.example_validator.component import ExampleValidator
from tfx.components.model_validator.component import ModelValidator
from tfx.components.pusher.component import Pusher
from tfx.components.schema_gen.component import SchemaGen
from tfx.components.statistics_gen.component import StatisticsGen
from tfx.components.trainer.component import Trainer
from tfx.components.transform.component import Transform
from tfx.orchestration.pipeline import Pipeline
from tfx.proto import trainer_pb2, evaluator_pb2, pusher_pb2, example_gen_pb2

from tfx.utils.dsl_utils import tfrecord_input
from tfx.components.example_gen.import_example_gen.component import ImportExampleGen


def create_pipeline(pipeline_name,
                    pipeline_root,
                    input_path,
                    tf_transform_file,
                    tf_trainer_file,
                    serving_model_basedir,
                    **kwargs):


    examples = tfrecord_input(input_path)

    input_config = example_gen_pb2.Input(splits=[
        example_gen_pb2.Input.Split(
            name='tfrecord', pattern='data_tfrecord-*.gz'), ])  # todo add as airflow var

    output_config = example_gen_pb2.Output(
        split_config=example_gen_pb2.SplitConfig(splits=[
            example_gen_pb2.SplitConfig.Split(
                name='train', hash_buckets=2),  # todo add as airflow var
            example_gen_pb2.SplitConfig.Split(
                name='eval', hash_buckets=1)  # todo add as airflow var
        ]))
    example_gen = ImportExampleGen(
        input_base=examples,
        input_config=input_config,
        output_config=output_config)

    statistics_gen = StatisticsGen(input_data=example_gen.outputs.examples)
    infer_schema = SchemaGen(stats=statistics_gen.outputs.output)
    validate_stats = ExampleValidator(
        stats=statistics_gen.outputs.output, schema=infer_schema.outputs.output)

    transform = Transform(
        input_data=example_gen.outputs.examples,
        schema=infer_schema.outputs.output,
        module_file=tf_transform_file)

    trainer = Trainer(
        module_file=tf_trainer_file,
        transformed_examples=transform.outputs.transformed_examples,
        schema=infer_schema.outputs.output,
        transform_output=transform.outputs.transform_output,
        train_args=trainer_pb2.TrainArgs(num_steps=10000),
        eval_args=trainer_pb2.EvalArgs(num_steps=5000))

    model_analyzer = Evaluator(
        examples=example_gen.outputs.examples,
        model_exports=trainer.outputs.output,
        feature_slicing_spec=evaluator_pb2.FeatureSlicingSpec(specs=[
            evaluator_pb2.SingleSlicingSpec(
                column_for_slicing=[])  # todo add your slicing column
        ]))

    model_validator = ModelValidator(
        examples=example_gen.outputs.examples, model=trainer.outputs.output)

    pusher = Pusher(
        model_export=trainer.outputs.output,
        model_blessing=model_validator.outputs.blessing,
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=serving_model_basedir)))

    pipeline = Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        **kwargs)
    pipeline.components = [example_gen,
                           statistics_gen,
                           infer_schema,
                           validate_stats,
                           transform,
                           trainer,
                           model_analyzer,
                           model_validator,
                           pusher]

    return pipeline
