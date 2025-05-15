from evodiff.pretrained import OA_DM_640M
import argparse
from typing import Callable, Optional

import numpy as np
import torch
import torch.nn as nn


def generate(
    input_string: str,
    tokenizer: Callable,
    model: nn.Module,
    DEVICE: torch.device,
    nonstandard_aas: bool = False,
    sampling_T: float = 1.0,
    repeat_penalty: Optional[float] = None,
    verbose: bool = True,
    seed: int = 0,
) -> str:
    
    # set seeds for reproducibility
    _ = torch.manual_seed(seed)
    np.random.seed(seed)

    # tokenizer variables
    possible_aas = tokenizer.all_aas + [tokenizer.mask]
    mask = tokenizer.mask_id
    BATCH_SIZE = 1  # this code only handles batch size of 1

    # Check if evodiff can sample non-standard AAs
    if nonstandard_aas:
        sample_aas = tokenizer.all_aas  # Include non-standard AAs
    else:
        sample_aas = tokenizer.all_aas[:-6]  # Limit sampling to standard 20 AAs

    # assert input sequence only contains mask or AA tokens
    assert all([i in possible_aas for i in input_string]), f"input string contains invalid tokens: {input_string}"

    # tokenize single sample
    sample = tokenizer.tokenize([input_string])

    # locations to unmask
    loc = np.where(sample == mask)[0]

    # move to device, add batch dim
    sample = torch.tensor(sample).to(DEVICE).unsqueeze(0)

    # Unmask 1 loc at a time randomly
    np.random.shuffle(loc)

    print("Initial seq: ", [tokenizer.untokenize(s) for s in sample][0])
    with torch.no_grad():
        for i in loc:
            timestep = torch.tensor([0] * BATCH_SIZE)  # placeholder but not called in OADM model
            timestep = timestep.to(DEVICE)
            prediction = model(sample, timestep)
            p = prediction[:, i, : len(sample_aas)]
            p = torch.nn.functional.softmax(p / sampling_T, dim=1)  # softmax over categorical probs
            p_sample = torch.multinomial(p, num_samples=1)

            # Repetition penalty
            if repeat_penalty is not None:  # ignore if value is None
                for j in range(BATCH_SIZE):  # iterate over each obj in batch
                    case1 = i == 0 and sample[j, i + 1] == p_sample[j]  # beginning of seq
                    case2 = i == len(sample[j]) - 1 and sample[j, i - 1] == p_sample[j]  # end of seq
                    case3 = (i < len(sample[j]) - 1 and i > 0) and (
                        (sample[j, i - 1] == p_sample[j]) or (sample[j, i + 1] == p_sample[j])
                    )  # middle of seq
                    if case1 or case2 or case3:
                        if verbose: 
                            print("Found repeat token, applying penalty")
                        p[j, int(p_sample[j])] /= repeat_penalty  # reduce prob of that token by penalty value
                        p_sample[j] = torch.multinomial(p[j], num_samples=1)  # resample
            sample[:, i] = p_sample.squeeze()
            if verbose:
                print([tokenizer.untokenize(s) for s in sample][0])
    return [tokenizer.untokenize(s) for s in sample][0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_string", type=str, default="############################", 
                       help="Input sequence with '#' as mask tokens to be filled. Use standard amino acid letters for fixed positions.")
    parser.add_argument("--gpu-id", type=int, default=None,
                       help="GPU device ID to use. If not specified, CPU will be used (slower).")
    parser.add_argument(
        "--nonstandard_aas",
        action="store_true",
        help="Include non-standard amino acids in sampling. Default: False (only standard 20 AAs). Enable only for specialized applications.",
    )
    parser.add_argument("--sampling_T", type=float, default=1.0, 
                       help="Temperature for sampling: higher values (>1.0) increase diversity, lower values (<1.0) increase conservatism. Default: 1.0")
    parser.add_argument(
        "--repeat_penalty",
        type=float,
        default=None,
        help="Penalty to reduce adjacent amino acid repeats. Recommended values: 1.2-2.0. Default: None (no penalty). Higher values more aggressively prevent repeats.",
    )
    parser.add_argument("--verbose", action="store_true", 
                       help="Print intermediate sequences during generation to monitor the design process. Default: False")

    args = parser.parse_args()
    if args.gpu_id is None:
        DEVICE = "cpu"
        print("Using CPU, if you want to use GPU, please specify --gpu-id")
    else:
        DEVICE = torch.device("cuda:" + str(args.gpu_id))
        torch.cuda.set_device(args.gpu_id)

    # Load pretrained model
    checkpoint = OA_DM_640M()
    model, _, tokenizer, _ = checkpoint
    model = model.to(DEVICE)
    model.eval()

    # Generate sequence
    design = generate(
        args.input_string,
        tokenizer,
        model,
        DEVICE,
        nonstandard_aas=args.nonstandard_aas,
        sampling_T=args.sampling_T,
        repeat_penalty=args.repeat_penalty,
        verbose=args.verbose
    )
    print("Final seq: ", design)


if __name__ == "__main__":
    main()
