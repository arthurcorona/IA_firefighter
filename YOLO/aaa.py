import torch
print(torch.cuda.is_available())  # Deve retornar True
print(torch.version.cuda)  # Deve exibir a versão do CUDA
