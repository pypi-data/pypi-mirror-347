import torch
import pkg_resources
import json
from evodiff.model import ByteNetLMTime, MSATransformerTime
from sequence_models.esm import MSATransformer
from sequence_models.constants import MSA_ALPHABET, PROTEIN_ALPHABET, ALL_AAS, PAD, MSA_PAD, MASK
from sequence_models.collaters import LMCollater
from evodiff.utils import Tokenizer, download_model
from evodiff.collaters import D3PMCollater, OAMaskCollater, ESMOAMaskCollater, D3PMCollaterMSA, ESMOAMaskCollaterMSA
from sequence_models.collaters import MSAAbsorbingCollater
import esm


def load_sequence_checkpoint(model_name, config_path, diffusion_timesteps, tokenizer=Tokenizer(), causal=False,
                         n_tokens = len(MSA_ALPHABET), path_to_checkpoints=None):
    with open(config_path, 'r') as f:
        config = json.load(f)
    d_embed = config['d_embed']
    d_model = config['d_model']
    n_layers = config['n_layers']
    kernel_size = config['kernel_size']
    r = config['r']
    masking_idx = tokenizer.mask_id
    if 'rank' in config:
        weight_rank = config['rank']
    else:
        weight_rank = None
    if 'slim' in config:
        slim = config['slim']
    else:
        slim = True
    if 'activation' in config:
        activation = config['activation']
    else:
        activation = 'relu'
    dropout=0.0
    tie_weights=False
    final_norm=True
    model = ByteNetLMTime(n_tokens, d_embed, d_model, n_layers, kernel_size, r,
                          causal=causal, padding_idx=masking_idx, rank=weight_rank, dropout=dropout,
                          tie_weights=tie_weights, final_ln=final_norm, slim=slim, activation=activation,
                          timesteps=diffusion_timesteps)
    if path_to_checkpoints is not None:
        state_dict = torch.load(path_to_checkpoints, map_location=torch.device('cpu'))
    else:
        state_dict = download_model(model_name)
    msd = state_dict['model_state_dict']
    if model_name == 'carp-640M' or model_name == 'carp-38M' or model_name == 'lrar-640M' or model_name=='lrar-38M':
        msd = {k.split('module.')[0]: v for k, v in msd.items()}
    else:
        msd = {k.split('module.')[1]: v for k, v in msd.items()}
    model.load_state_dict(msd)

    return model, tokenizer

def load_msa_checkpoint(model_name, config_path, diffusion_timesteps, tokenizer=Tokenizer()):
    with open(config_path, 'r') as f:
        config = json.load(f)
    d_embed = config['d_embed']
    d_hidden = config['d_hidden']
    n_layers = config['n_layers']
    n_heads = config['n_heads']
    if diffusion_timesteps is None:
        model = MSATransformer(d_embed, d_hidden, n_layers, n_heads, use_ckpt=True, n_tokens=len(MSA_ALPHABET),
                               padding_idx=MSA_ALPHABET.index(MSA_PAD), mask_idx=MSA_ALPHABET.index(MASK))
    else:
        padding_idx = tokenizer.pad_id
        masking_idx = tokenizer.mask_id
        model = MSATransformerTime(d_embed, d_hidden, n_layers, n_heads, timesteps=diffusion_timesteps, use_ckpt=True,
                               n_tokens=len(MSA_ALPHABET), padding_idx=padding_idx, mask_idx=masking_idx)
    state_dict = download_model(model_name)
    # sd = torch.load(state_dict, map_location=torch.device('cpu'))
    msd = state_dict['model_state_dict']
    if model_name == 'carp-640M' or model_name == 'carp-38M':
        msd = {k.split('module.')[0]: v for k, v in msd.items()}
    else:
        msd = {k.split('module.')[1]: v for k, v in msd.items()}
    model.load_state_dict(msd)
    return model, tokenizer

def D3PM_BLOSUM_640M(return_all=False):
    dt=500
    tokenizer = Tokenizer(path_to_blosum="data/blosum62-special-MSA.mat", sequences=True)
    Q_prod, Q_t = tokenizer.q_blosum_schedule(timesteps=dt)
    collater = D3PMCollater(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'config640M.json')
    # file_path = 'config/config640M.json'
    model, tokenizer = load_sequence_checkpoint("d3pm-blosum-640M", file_path,
                                                      diffusion_timesteps=dt,
                                                      tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme

def D3PM_BLOSUM_38M(return_all=False):
    dt=500
    tokenizer = Tokenizer(path_to_blosum="data/blosum62-special-MSA.mat", sequences=True)
    Q_prod, Q_t = tokenizer.q_blosum_schedule(timesteps=dt)
    collater = D3PMCollater(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'config38M.json')
    model, tokenizer = load_sequence_checkpoint("d3pm-blosum-38M", file_path,
                                                      diffusion_timesteps=dt,
                                                      tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme

def D3PM_UNIFORM_640M(return_all=False):
    dt = 500
    tokenizer = Tokenizer(sequences=True)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollater(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'config640M.json')
    # file_path = 'config/config640M.json'
    model, tokenizer = load_sequence_checkpoint("d3pm-uniform-640M", file_path, diffusion_timesteps=dt,
                                            tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme


def D3PM_UNIFORM_38M(return_all=False):
    dt = 500
    tokenizer = Tokenizer(sequences=True)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollater(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'config38M.json')
    model, tokenizer = load_sequence_checkpoint("d3pm-uniform-38M", file_path, diffusion_timesteps=dt,
                                            tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme


def OA_DM_640M(path_to_checkpoints=None):
    tokenizer = Tokenizer()
    collater = OAMaskCollater(tokenizer=tokenizer)
    file_path = pkg_resources.resource_filename('config', 'config640M.json')
    # file_path = 'config/config640M.json'
    model, tokenizer = load_sequence_checkpoint("oaar-640M", file_path, diffusion_timesteps=None, \
                         tokenizer=tokenizer, n_tokens=len(MSA_ALPHABET), path_to_checkpoints=path_to_checkpoints)
    scheme = 'mask'
    return model, collater, tokenizer, scheme


def OA_DM_38M():
    tokenizer = Tokenizer()
    collater = OAMaskCollater(tokenizer=tokenizer)
    file_path = pkg_resources.resource_filename('config', 'config38M.json')
    model, tokenizer = load_sequence_checkpoint("oaar-38M", file_path, diffusion_timesteps=None, \
                         tokenizer=tokenizer)
    scheme = 'mask'
    return model, collater, tokenizer, scheme


def LR_AR_640M():
    n_tokens = len(PROTEIN_ALPHABET)
    tokenizer = Tokenizer(protein_alphabet=PROTEIN_ALPHABET, all_aas=ALL_AAS, pad=PAD)
    collater = LMCollater(PROTEIN_ALPHABET)
    file_path = pkg_resources.resource_filename('config', 'config640M.json')
    # file_path = 'config/config640M.json'
    model, tokenizer = load_sequence_checkpoint("lrar-640M", file_path, diffusion_timesteps=None, \
                                tokenizer=tokenizer, causal=True, n_tokens=n_tokens)
    scheme='causal-mask'
    return model, collater, tokenizer, scheme


def LR_AR_38M():
    n_tokens = len(PROTEIN_ALPHABET)
    tokenizer = Tokenizer(protein_alphabet=PROTEIN_ALPHABET, all_aas=ALL_AAS, pad=PAD)
    collater = LMCollater(PROTEIN_ALPHABET)
    file_path = pkg_resources.resource_filename('config', 'config38M.json')
    model, tokenizer = load_sequence_checkpoint("lrar-38M", file_path, diffusion_timesteps=None, \
                                tokenizer=tokenizer, causal=True, n_tokens=n_tokens)
    scheme='causal-mask'
    return model, collater, tokenizer, scheme

def CARP_38M():
    n_tokens = len(PROTEIN_ALPHABET)
    tokenizer = Tokenizer(protein_alphabet=PROTEIN_ALPHABET, all_aas=ALL_AAS, pad=PAD)
    collater = OAMaskCollater(tokenizer=tokenizer)
    file_path = pkg_resources.resource_filename('config', 'config38M.json')
    model, tokenizer = load_sequence_checkpoint("carp-38M", file_path, diffusion_timesteps=None, \
                                tokenizer=tokenizer, causal=False, n_tokens=n_tokens)
    scheme='mask'
    return model, collater, tokenizer, scheme

def CARP_640M():
    n_tokens = len(PROTEIN_ALPHABET)
    tokenizer = Tokenizer(protein_alphabet=PROTEIN_ALPHABET, all_aas=ALL_AAS, pad=PAD)
    collater = OAMaskCollater(tokenizer=tokenizer)
    file_path = pkg_resources.resource_filename('config', 'config640M.json')
    # file_path = 'config/config640M.json'
    model, tokenizer = load_sequence_checkpoint("carp-640M", file_path, diffusion_timesteps=None, \
                                tokenizer=tokenizer, causal=False, n_tokens=n_tokens)
    scheme='mask'
    return model, collater, tokenizer, scheme

def ESM1b_650M():
    "Wrapper for ESM model"
    model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
    collater = ESMOAMaskCollater(alphabet=alphabet)
    scheme='esm-mask'
    return model, collater, alphabet, scheme

def ESM2_650M():
    "Wrapper for ESM model"
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    collater = ESMOAMaskCollater(alphabet=alphabet)
    scheme='esm-mask'
    return model, collater, alphabet, scheme

def MSA_D3PM_BLOSUM_RANDSUB(return_all=False):
    dt = 500
    tokenizer = Tokenizer(path_to_blosum="data/blosum62-special-MSA.mat", sequences=False)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollaterMSA(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-d3pm-blosum-randsub", file_path,
                                                diffusion_timesteps=dt,
                                                tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme

def MSA_D3PM_BLOSUM_MAXSUB(return_all=False):
    dt = 500
    tokenizer = Tokenizer(path_to_blosum="data/blosum62-special-MSA.mat", sequences=False)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollaterMSA(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-d3pm-blosum-maxsub", file_path,
                                                diffusion_timesteps=dt,
                                                tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme

def MSA_D3PM_UNIFORM_RANDSUB(return_all=False):
    dt = 500
    tokenizer = Tokenizer(sequences=False)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollaterMSA(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-d3pm-uniform-randsub", file_path,
                                                diffusion_timesteps=dt,
                                                tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme

def MSA_D3PM_UNIFORM_MAXSUB(return_all=False):
    dt = 500
    tokenizer = Tokenizer(sequences=False)
    Q_prod, Q_t = tokenizer.q_random_schedule(timesteps=dt)
    collater = D3PMCollaterMSA(tokenizer=tokenizer, num_timesteps=dt, Q=Q_t, Q_bar=Q_prod)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-d3pm-uniform-maxsub", file_path,
                                                diffusion_timesteps=dt,
                                                tokenizer=tokenizer)
    scheme = 'd3pm'
    if return_all:
        return model, collater, tokenizer, scheme, dt, Q_prod, Q_t
    else:
        return model, collater, tokenizer, scheme


def MSA_OA_DM_RANDSUB():
    tokenizer = Tokenizer()
    collater = MSAAbsorbingCollater(alphabet=MSA_ALPHABET)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-oaar-randsub", file_path,
                                           diffusion_timesteps=None,
                                           tokenizer=tokenizer)
    scheme = 'mask'
    return model, collater, tokenizer, scheme

def MSA_OA_DM_MAXSUB():
    tokenizer = Tokenizer()
    collater = MSAAbsorbingCollater(alphabet=MSA_ALPHABET)
    file_path = pkg_resources.resource_filename('config', 'configMSA.json')
    # file_path = 'config/configMSA.json'
    model, tokenizer = load_msa_checkpoint("msa-oaar-maxsub", file_path,
                                           diffusion_timesteps=None,
                                           tokenizer=tokenizer)
    scheme = 'mask'
    return model, collater, tokenizer, scheme

def ESM_MSA_1b():
    "Wrapper for ESM model"
    model, alphabet = esm.pretrained.esm_msa1b_t12_100M_UR50S()
    collater = ESMOAMaskCollaterMSA(alphabet=alphabet)
    scheme='esm-mask'
    return model, collater, alphabet, scheme

