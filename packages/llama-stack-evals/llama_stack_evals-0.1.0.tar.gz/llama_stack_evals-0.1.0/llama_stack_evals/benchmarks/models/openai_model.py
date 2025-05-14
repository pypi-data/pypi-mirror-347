# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import json
import os
import time
from typing import Any

from openai import OpenAI

from .interface import Dialog, IModel


class OpenAIModel(IModel):
    """Call any OpenAI compatible API endpoint."""

    def __init__(
        self,
        model_id: str,
        system_message: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        self.model_id = model_id
        self.system_message = system_message
        self.base_url = base_url
        self.api_key = api_key
        self.client = None
        self.error_file = None
        if os.environ.get("ERROR_LOG_FILE"):
            self.error_file = open(os.environ["ERROR_LOG_FILE"], "a")

    def minibatch_size(self) -> int:
        return 1

    def generate(
        self,
        dialog_minibatch: list[Dialog],
        *,
        temperature: float,
        max_tokens: int,
        top_p: float | None,
        tools: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        assert len(dialog_minibatch) == 1, "OpenAI model currently only supports batching one dialog at a time"
        if not self.client:
            self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

        dialog = dialog_minibatch[0]
        if self.system_message:
            dialog = [
                {"role": "system", "content": self.system_message},
            ] + dialog

        trial = 0
        while True:
            try:
                params = {
                    "model": self.model_id,
                    "messages": dialog,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                if tools:
                    params["tools"] = tools
                if top_p is not None:
                    params["top_p"] = top_p
                response = self.client.chat.completions.create(**params)
                return [response.choices[0].message.content]
            except Exception as e:
                sleep_time = 4 + 1.5**trial
                print(f"Error generating response: {e}. Sleep for {sleep_time} seconds")
                time.sleep(sleep_time)
                trial += 1
                if trial > int(os.getenv("MAX_RETRIES", 6)):
                    if self.error_file:
                        d = json.dumps(
                            {
                                "error": str(e),
                                "params": params,
                            }
                        )
                        self.error_file.write(d + "\n")
                    # use an easy to grep error message
                    return [f"INFERENCE_ERROR: {e}"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.model_id})"
