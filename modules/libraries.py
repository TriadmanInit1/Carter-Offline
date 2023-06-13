import requests
import json
from ai_config import *
import pyttsx3

import whisper
import pyaudio
import wave

from scipy.io import wavfile
import noisereduce as nr

import os
import nextcord as discord

from art import text2art

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from modules.nltk_utils import bag_of_words, tokenize, stem
from modules.model import NeuralNet

from modules.model import NeuralNet
from modules.nltk_utils import bag_of_words, tokenize

import nltk
from nltk.metrics.distance import edit_distance

from nltk.tokenize import word_tokenize

from torch.nn.functional import cosine_similarity

import time

import numpy as np
