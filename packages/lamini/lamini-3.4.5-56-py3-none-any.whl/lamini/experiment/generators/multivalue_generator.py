from lamini.experiment.generators.base_generator import BaseGenerator
from lamini.generation.base_prompt_object import PromptObject
from copy import deepcopy
import re

import json


class MultiValueGenerator(BaseGenerator):
    """A generator that takes a single prompt and returns a list of outputs.

    Main change from the base generator is that it returns a list of ExperimentObjects
    from the postprocess method. All other functionality is the same as the base generator.

    Parameters
    ----------
    model : object
        The model to use for the generator.
    client : object, optional
        The client to use for the generator.
    name : str, optional
        The name of the generator.
    role : str, optional
        The role of the generator.
    instruction : str, optional
        The instruction to use for the generator.
    output_type : dict, optional
        The output type of the generator.
    subkey_output_type : str, optional
        The subkey output type of the generator.
    postprocess_delimiter : str, optional
        The delimiter to use for the postprocess method. Default is ",".
    **kwargs
        Additional keyword arguments.
    """

    def __init__(
        self,
        model,
        client=None,
        name=None,
        role=None,
        instruction=None,
        output_type=None,
        subkey_output_type=None,
        **kwargs,
    ):
        name = name or "MultiValueGenerator"

        super().__init__(
            client=client,
            model=model,
            name=name,
            role=role,
            instruction=instruction,
            output_type=output_type,
            **kwargs,
        )

        self.subkey_output_type = subkey_output_type
        self.output = {subkey_output_type: output_type[list(output_type.keys())[0]]}
        self.output_key = output_type

    def postprocess(self, result):
        """Process a dictionary result into a list of ExperimentObjects.

        Takes an ExperimentObject with a dictionary response and creates multiple
        ExperimentObjects, one for each key in self.output_type. Each new object
        contains the original prompt and data, with an additional field specified
        by self.subkey_output_type containing the corresponding value from
        self.output_type.

        Parameters
        ----------
        result : ExperimentObject
            An ExperimentObject containing a response that should be a dictionary

        Returns
        -------
        list of ExperimentObject
            A list of new ExperimentObjects, each containing the original data plus
            a new field specified by self.subkey_output_type. The value of this field
            comes from self.output_type[key] for each key in self.output_type.
            Returns an empty list if the response is not a dictionary.

        Notes
        -----
        The method:
        1. Checks if the response is a dictionary
        2. For each key in self.output_type:
           - Creates a deep copy of the original ExperimentObject
           - Adds a new field using self.subkey_output_type as the key and
             self.output_type[key] as the value
        3. Returns the list of new ExperimentObjects
        """

        raw = result.response
        if raw is None:
            self.logger.warning(f"[{self.name}] empty response")
            return []

        # 1️⃣  strip markdown fences
        if isinstance(raw, str) and raw.lstrip().startswith("```"):
            raw = re.sub(r"^```.*?\n|\n```$", "", raw.strip(), flags=re.S)

        # 2️⃣  parse JSON or fallback to line-split
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
            except Exception:
                # plain text, split per line
                lines = [
                    ln.strip("-•* ").strip() for ln in raw.splitlines() if ln.strip()
                ]
                parsed = {
                    k: lines[i]
                    for i, k in enumerate(self.output_type)
                    if i < len(lines)
                }
        elif isinstance(raw, dict):
            parsed = raw
        else:
            self.logger.error(f"[{self.name}] unknown response type: {type(raw)}")
            return []

        # 3️⃣  build children
        children = []
        for k in self.output_type.keys():
            if k not in parsed or not parsed[k]:
                continue
            child = PromptObject(
                prompt=deepcopy(result.prompt),
                data=deepcopy(result.data),
                response=parsed,
            )
            # copy the *actual* answer, not the schema stub!
            child.data[self.subkey_output_type] = parsed[k]
            children.append(child)
        return children
