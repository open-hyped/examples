from hyped.data.flow.processors.ops.noop import NoOp, NoOpInputRefs
from hyped.data.flow.processors.templates.jinja2 import Jinja2, Jinja2Config
from hyped.data.flow.ops import collect
from hyped.data.flow.flow import DataFlow
import datasets
import numpy as np

datasets.disable_caching()

ds = datasets.Dataset.from_dict({
    "This is a feature with blanks.": [0, 1],
    "text": ["ABCDEFG", "HIJKLMNOP"],
})

flow = DataFlow(ds.features)

template_str = """This is a Jinja2 template using the feature "text" with value "{{ inputs.text }}".
Another feature is "label_name", which has value {{ inputs["label_name"] }}"""

jinja2 = Jinja2(Jinja2Config(template=template_str))
jinja2_out = jinja2.call(
    features=collect({
        "text": flow.src_features.text,
        "label_name": flow.src_features["This is a feature with blanks."],
    })
)

jinja2_out2 = jinja2.call(
    features=collect({
        "text": flow.src_features.text,
        "label_name": flow.src_features.text,
    })
)

output_features = collect({
    "text": flow.src_features.text,
    "prompt1": jinja2_out.parsed,
    "prompt2": jinja2_out2.parsed,
})
ds_out = flow.apply(ds, collect=output_features)

print(ds_out[0])
