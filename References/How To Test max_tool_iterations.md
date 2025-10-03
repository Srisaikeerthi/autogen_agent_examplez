# Sample Prompts to Verify max_tool_iterations in example5_custom_tools

Based on the AutoGen code analysis, here are sample prompts to verify the `max_tool_iterations` functionality:

## Basic Iteration Tests

**Prompt 1: Single iteration requirement**

```
"Calculate the area of a circle with radius 7"
```

This should use only 1 tool call (within the default `max_tool_iterations=3`).

**Prompt 2: Multiple sequential tool calls**

```
"Roll 2 dice, then calculate the area of a circle using the first dice result as the radius, then give me a random fact"
```

This requires 3 sequential tool calls and should work with `max_tool_iterations=3`.

**Prompt 3: Exceeding iteration limit**

```
"Roll dice 5 times, calculate the area of circles using each result as radius, then give me 3 random facts"
```

This would require 8+ tool calls and should stop at the `max_tool_iterations=3` limit.

## Chain-Dependent Operations

**Prompt 4: Dependent calculations**

```
"Roll a 10-sided dice, then calculate the area of a circle with that radius, then roll that many 6-sided dice and tell me the total"
```

This creates a chain where each tool call depends on the previous result.

**Prompt 5: Mathematical progression**

```
"Start by rolling a dice, then calculate a circle area with that radius, then use the area as the number of sides for another dice roll"
```

This tests whether the agent can maintain context across multiple iterations.

## Iteration Limit Testing

**Prompt 6: Explicit counting request**

```
"Count from 1 to 5 by: rolling a dice for each number, calculating circle areas, and giving random facts alternately"
```

This clearly exceeds 3 iterations and will test the stopping behavior.

**Prompt 7: Complex multi-step task**

```
"Please do the following in order: 1) Roll dice twice, 2) Calculate areas for both results, 3) Roll dice equal to the sum of areas, 4) Give me facts about each dice result, 5) Calculate one final area"
```

This definitely exceeds the limit and tests early termination.

## Expected Behaviors

With `max_tool_iterations=3`, the agent will:

- Execute up to 3 rounds of tool calls before stopping
- Stop early if the model produces a non-tool response
- Return partial results when hitting the iteration limit
- Continue processing until either condition is met


## Testing Different Limits

To test different iteration limits, modify the agent configuration:

```python
# Test with 1 iteration limit
tool_agent = AssistantAgent(
    name="tool_master",
    model_client=model_client,
    tools=[calculate_circle_area, roll_dice, get_random_fact],
    max_tool_iterations=1,  # Only 1 iteration allowed
)

# Test with 5 iteration limit
tool_agent = AssistantAgent(
    name="tool_master",
    model_client=model_client,
    tools=[calculate_circle_area, roll_dice, get_random_fact],
    max_tool_iterations=5,  # Up to 5 iterations allowed
)
```

The agent stops when either the model returns a text response instead of tool calls, or the maximum number of iterations is reached.
