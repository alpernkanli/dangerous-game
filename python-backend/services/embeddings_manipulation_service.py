import torch

class ManipulationService:
    def __init__(self):
        pass

    def add_noise(self, embedding: torch.Tensor, noise_level: float = 0.1, method: str = "gaussian") -> torch.Tensor:
        """
        Adds noise or perturbation to an embedding.
        Args:
            embedding (torch.Tensor): Input embedding to perturb.
            noise_level (float): Standard deviation (Gaussian) or range (Uniform) of the noise.
            method (str): Type of noise to add ("gaussian" or "uniform").
        Returns:
            torch.Tensor: Perturbed embedding.
        """
        if method == "gaussian":
            noise = torch.randn_like(embedding) * noise_level
        elif method == "uniform":
            noise = torch.empty_like(embedding).uniform_(-noise_level, noise_level)
        else:
            raise ValueError(f"Unsupported noise method: {method}. Use 'gaussian' or 'uniform'.")

        return embedding + noise

    def remix_slerp(self, a: torch.Tensor, b: torch.Tensor, n: float, eps: float = 1e-8) -> torch.Tensor:
        """
        Performs Spherical Linear Interpolation (SLERP) between two embeddings.
        Args:
            a (torch.Tensor): Starting embedding.
            b (torch.Tensor): Target embedding.
            n (float): Interpolation factor (0.0 = a, 1.0 = b).
            eps (float): Small value to avoid numerical issues.
        Returns:
            torch.Tensor: Interpolated embedding.
        """
        a_norm = a / (torch.norm(a) + eps)
        b_norm = b / (torch.norm(b) + eps) 
        omega = torch.acos((a_norm * b_norm).sum(dim=-1).clamp(-1 + eps, 1 - eps))
        so = torch.sin(omega)
        
        if torch.isclose(so, torch.tensor(0.0)):
            return (1.0 - n) * a + n * b
        
        return (torch.sin((1.0 - n) * omega) / so) * a + (torch.sin(n * omega) / so) * b
