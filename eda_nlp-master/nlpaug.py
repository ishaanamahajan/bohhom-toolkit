import nlpaug.augmenter.word as naw

syn_aug = naw.SynonymAug(aug_p=0.3)
sentence = 'climate change puts the squeeze on wine production'
mod_sentence = syn_aug.augment(sentence, n=1)
print('Original text :', sentence)
print('Augmented text :', mod_sentence)