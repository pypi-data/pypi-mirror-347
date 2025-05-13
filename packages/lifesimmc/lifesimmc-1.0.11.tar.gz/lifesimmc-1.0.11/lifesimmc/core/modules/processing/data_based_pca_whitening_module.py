from itertools import product

import numpy as np
import torch
from matplotlib import pyplot as plt
from numpy.linalg import inv
from scipy.linalg import sqrtm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from lifesimmc.core.modules.processing.base_transformation_module import BaseTransformationModule
from lifesimmc.core.resources.base_resource import BaseResource
from lifesimmc.core.resources.data_resource import DataResource
from lifesimmc.core.resources.template_resource import TemplateResource
from lifesimmc.core.resources.transformation_resource import TransformationResource


class DataBasedPCAWhiteningModule(BaseTransformationModule):
    """Class representation of the ZCA whitening transformation module. This module applied ZCA whitening to the data
    and templates using a covariance matrix based on a calibration star. The properties of this calibration star are
    assumed to be identical to the properties of the target star.

    Parameters
    ----------

    n_setup_in : str
        Name of the input configuration resource.
    n_data_in : str
        Name of the input data resource.
    n_template_in : str
        Name of the input template resource.
    n_data_out : str
        Name of the output data resource.
    n_template_out : str
        Name of the output template resource.
    n_transformation_out : str
        Name of the output transformation resource.
    diagonal_only : bool
        If True, only the diagonal of the covariance matrix is used for whitening. Default is False.
    """

    def __init__(
            self,
            n_setup_in: str,
            n_data_in: str,
            n_data_out: str,
            n_transformation_out: str,
            n_template_in: str = None,
            n_template_out: str = None,
            diagonal_only: bool = False
    ):
        """Constructor method.

        Parameters
        ----------
        n_setup_in : str
            Name of the input configuration resource.
        n_data_in : str
            Name of the input data resource.
        n_template_in : str
            Name of the input template resource.
        n_data_out : str
            Name of the output data resource.
        n_template_out : str
            Name of the output template resource.
        n_transformation_out : str
            Name of the output transformation resource.
        diagonal_only : bool
            If True, only the diagonal of the covariance matrix is used for whitening. Default is False.
        """
        super().__init__()
        self.n_config_in = n_setup_in
        self.n_data_in = n_data_in
        self.n_template_in = n_template_in
        self.n_data_out = n_data_out
        self.n_template_out = n_template_out
        self.n_transformation_out = n_transformation_out
        self.diagonal_only = diagonal_only

    def apply(self, resources: list[BaseResource]) -> tuple[DataResource, TemplateResource, TransformationResource]:
        """Apply the module.

        Parameters
        ----------
        resources : list[BaseResource]
            List of resources to be processed.

        Returns
        -------
        tuple[DataResource, TemplateResource, TransformationResource]
            Tuple containing the output data resource, template resource, and transformation resource.
        """
        print('Applying ZCA whitening...')

        config_in = self.get_resource_from_name(self.n_config_in)

        # # # Generate a calibration star data set
        # # if self.seed is None:
        # #     seed = torch.randint(0, 2 ** 31, (1,)).item()
        # # else:
        # #     seed = (self.seed + 1) * 2
        # #     if seed > 2 ** 31:
        # #         seed = seed // 10
        # #
        # # self.seed = seed
        # # torch.manual_seed(seed)
        # # torch.cuda.manual_seed(seed)
        # # torch.cuda.manual_seed_all(seed)
        # # np.random.seed(seed)
        # #
        # # phringe = PHRINGE(
        # #     seed=self.seed,
        # #     gpu_index=self.gpu_index,
        # #     grid_size=self.grid_size,
        # #     time_step_size=self.time_step_size,
        # #     device=self.device,
        # #     extra_memory=20
        # # )
        #
        # # Create a copy of the instrument and add draw new perturbation time series
        # inst = config_in.instrument
        # amplitude_pert = inst.perturbations.amplitude
        # phase_pert = inst.perturbations.phase
        # polarization_pert = inst.perturbations.polarization
        #
        # inst_new = copy(inst)
        #
        # if amplitude_pert.rms is not None:
        #     inst_new.remove_perturbation(amplitude_pert)
        #     amplitude_pert_new = AmplitudePerturbation(rms=amplitude_pert.rms, color=amplitude_pert.color)
        #     inst_new.add_perturbation(amplitude_pert_new)
        #
        # if phase_pert.rms is not None:
        #     inst_new.remove_perturbation(phase_pert)
        #     phase_pert_new = PhasePerturbation(rms=phase_pert.rms, color=phase_pert.color)
        #     inst_new.add_perturbation(phase_pert_new)
        #
        # if polarization_pert.rms is not None:
        #     inst_new.remove_perturbation(polarization_pert)
        #     polarization_pert_new = PolarizationPerturbation(rms=polarization_pert.rms, color=polarization_pert.color)
        #     inst_new.add_perturbation(polarization_pert_new)
        #
        # phringe.set(inst_new)
        #
        # # Set the observation
        # phringe.set(config_in.observation)
        #
        # # Remove all planets from the scene to calculate covariance only on noise
        # scene_new = copy(config_in.scene)
        # for planet in config_in.scene.planets:
        #     scene_new.remove_source(planet.name)
        # phringe.set(scene_new)

        # # Get the differential counts for the calibration star
        # diff_counts = phringe.get_diff_counts()
        data_in = self.get_resource_from_name(self.n_data_in).get_data()
        # diff_counts = copy(data_in)
        diff_counts = torch.zeros(data_in.shape, device=self.device, dtype=torch.float32)

        # Calculate the whitening matrix
        cov = torch.zeros(
            (diff_counts.shape[0], diff_counts.shape[1], diff_counts.shape[1]),
            device=self.device,
            dtype=torch.float32
        )
        icov2 = torch.zeros(
            (diff_counts.shape[0], diff_counts.shape[1], diff_counts.shape[1]),
            device=self.device,
            dtype=torch.float32
        )

        # ####################
        # PCA subtraction
        pc = 5

        # Standardizing the data
        scaler = StandardScaler()
        data_std = scaler.fit_transform(data_in[0].cpu().numpy().T)

        # Performing PCA
        pca = PCA(n_components=data_std.shape[1])  # Use min to avoid exceeding dimensions
        principal_components = pca.fit_transform(data_std)

        # Zero out the first 10 components
        principal_components[:, pc:] = np.zeros(principal_components[:, pc:].shape)

        # Reconstruct the data from modified principal components
        data_low_rank = pca.inverse_transform(principal_components)

        # Reversing the standardization
        data_low_rank = torch.tensor(
            scaler.inverse_transform(data_low_rank),
            device=self.device,
            dtype=torch.float32
        ).T

        plt.imshow(data_low_rank.cpu().numpy())
        plt.colorbar()
        plt.show()

        # #############

        for i in range(len(diff_counts)):
            # fit data and get cov from this

            cov[i] = torch.cov(data_low_rank)
            icov2[i] = torch.tensor(sqrtm(inv(cov[i].cpu().numpy())), device=self.device, dtype=torch.float32)

            ##############
            # PCA whitening

            # eigendecomposition
            # eigenvalues, eigenvectors = np.linalg.eig(cov[i].cpu().numpy())
            #
            # # Create the diagonal matrix Lambda from eigenvalues
            # Lambda = np.diag(eigenvalues)
            #
            # # Inverse of the eigenvector matrix
            # V_inv = np.linalg.inv(eigenvectors)
            #
            # plt.imshow(cov[i].cpu().numpy())
            # plt.colorbar()
            # plt.show()
            #
            # # plt.imshow(sqrtm(inv(cov[i].cpu().numpy())))
            # # plt.colorbar()
            # # plt.show()
            #
            # w_pca = sqrtm(inv(Lambda)) @ V_inv
            #
            # w_pca = torch.tensor(w_pca, device=self.device, dtype=torch.float32)

            # # set the first 10 elements in both dimensions to zero from cov
            # x_max = 2  # das kannst du ändern
            #
            # # Maske: alle Punkte mit i + j <= x_max
            # ny, nx = cov[i].shape
            # y, x = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
            # mask = (x + y) <= x_max
            #
            # for j in range(len(cov[i])):
            #     mask[j][j] = 1
            # # Set everything else to 0
            # # cov[i][~mask] = 0

            # plt.imshow(mask)
            # plt.colorbar()
            # plt.show()

            # plt.imshow(cov[i].cpu().numpy())
            # plt.colorbar()
            # plt.show()
            #
            # plt.imshow(inv(cov[i].cpu().numpy()))
            # plt.colorbar()
            # plt.show()

            # Setze den Bereich im Dreieck auf 0
            # cov[i][mask] = 0
            #
            # i_cov_sqrt[i] = torch.tensor(sqrtm(inv(cov[i].cpu().numpy())), device=self.device, dtype=torch.float32)
            #
            # plt.imshow(i_cov_sqrt[i].cpu().numpy())
            # plt.colorbar()
            # plt.show()

        # Apply the whitening matrix to the data and templates
        r_data_out = DataResource(self.n_data_out)

        for i in range(data_in.shape[0]):
            data_in[i] = icov2 @ data_in[i]

            plt.imshow(data_in[i].cpu().numpy())
            plt.colorbar()
            plt.show()

        r_data_out.set_data(data_in)

        if self.n_template_in and self.n_template_out:
            r_template_in = self.get_resource_from_name(self.n_template_in)
            template_data_in = r_template_in.get_data()
            template_counts_white = torch.zeros(template_data_in.shape, device=self.device, dtype=torch.float32)

            for i, j in tqdm(
                    product(range(template_data_in.shape[-2]), range(template_data_in.shape[-1])),
                    total=template_data_in.shape[-2] * template_data_in.shape[-1]
            ):
                for k in range(template_data_in.shape[0]):
                    template_counts_white[k, :, :, i, j] = icov2 @ template_data_in[k, :, :, i, j]

            r_template_out = TemplateResource(
                name=self.n_template_out,
                grid_coordinates=r_template_in.grid_coordinates
            )
            r_template_out.set_data(template_counts_white)
        else:
            r_template_out = None

        # Save the whitening transformation
        def zca_whitening_transformation(data):
            """Apply the ZCA whitening transformation."""
            if isinstance(data, np.ndarray):
                i2 = icov2.cpu().numpy()
            else:
                i2 = icov2
            for l in range(data.shape[0]):
                data[l] = i2 @ data[l]
            return data

        zca = zca_whitening_transformation

        r_transformation_out = TransformationResource(
            name=self.n_transformation_out,
            transformation=zca
        )

        print('Done')
        if r_template_out is not None:
            return r_data_out, r_template_out, r_transformation_out
        return r_data_out, r_transformation_out
