"""
Projects API endpoints
"""

from .base import BaseAPI


class ProjectsAPI(BaseAPI):
    """
    Projects API endpoints

    This class provides methods for interacting with the Frekil Projects API.
    """

    def list(self):
        """
        List all projects the authenticated user has access to

        Returns:
            list: List of projects
        """
        return self.client.get("api/sdk/projects/")

    def get_membership(self, project_id):
        """
        Get membership details for a specific project including user roles and status

        Args:
            project_id (str): The project ID

        Returns:
            list: List of project memberships
        """
        return self.client.get(f"api/sdk/projects/{project_id}/membership/")

    def bulk_allocate_images(
        self, project_id, allocations, override_existing_work=False
    ):
        """
        Bulk allocate images to specific annotators and reviewers

        Args:
            project_id (str): The project ID
            allocations (list): List of allocation objects with the following structure:
                {
                    "image_key": "image1.jpg",
                    "annotators": ["annotator1@example.com", "annotator2@example.com"],
                    "reviewers": ["reviewer1@example.com", "reviewer2@example.com"]
                }
            override_existing_work (bool, optional): Whether to override existing work.
                Defaults to False.

        Returns:
            dict: Result of the allocation operation
        """
        data = {
            "allocations": allocations,
            "override_existing_work": override_existing_work,
        }

        return self.client.post(
            f"api/sdk/projects/{project_id}/bulk-allocate/", json=data
        )
