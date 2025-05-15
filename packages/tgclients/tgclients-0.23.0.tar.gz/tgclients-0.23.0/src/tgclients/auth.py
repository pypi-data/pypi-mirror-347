# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Provide access to the TextGrid Authorization Service."""

import logging
from typing import List, Optional

from zeep import Client
from zeep.exceptions import Fault, TransportError

from tgclients.config import TextgridConfig

TG_STANDARD_ROLE_MANAGER = 'Projektleiter'
TG_STANDARD_ROLE_ADMINISTRATOR = 'Administrator'
TG_STANDARD_ROLE_EDITOR = 'Bearbeiter'
TG_STANDARD_ROLE_OBSERVER = 'Beobachter'

logger = logging.getLogger(__name__)
# prevent the zeep "Forcing soap:address location to HTTPS" warning
logging.getLogger('zeep.wsdl.bindings.soap').setLevel(logging.ERROR)


class TextgridAuth:
    """Provide access to the TextGrid Authorization Service."""

    def __init__(self, config: TextgridConfig = TextgridConfig()) -> None:
        self._config = config
        self._client = self._connect()
        self._extra_crud_client = self._connect_extra_crud()

    def _connect(self) -> Client:
        """Create standard SOAP client.

        Internal helper that provides a SOAP client that is configured for
        the use with the Textgrid Auth service.

        Returns:
            Client: A SOAP client
        """
        client = Client(self._config.auth_wsdl)
        # this is a dirty hack; should be remediated
        client.service._binding_options['address'] = self._config.auth_address
        return client

    def _connect_extra_crud(self) -> Client:
        """Create tgextra SOAP client.

        Internal helper that provides a SOAP client that is configured for
        the use with the Textgrid Auth service (the extra crud service).

        Returns:
            Client: A SOAP client
        """
        client = Client(self._config.extra_crud_wsdl)
        # this is a dirty hack; should be remediated
        client.service._binding_options['address'] = self._config.extra_crud_address
        return client

    def list_assigned_projects(self, sid: str) -> List[str]:
        """Get assigned projects.

        Args:
            sid (str): Session ID

        Raises:
            TextgridAuthException: in case of transport exceptions

        Returns:
            List[str]: A list of project id strings
        """
        try:
            return self._client.service.tgAssignedProjects(sid)
        except TransportError as error:
            message = 'Error listing assigned projects. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error

    def list_all_projects(self) -> List[str]:
        """List all projects.

        Returns all projects stored in this RBAC instance with ID, name,
        and description. See also getProjectDescription(). SID
        is not needed as this information can be reviewed publicly.

        Returns:
            List[str]: list of each project with ID, name and description
        """
        # sid is optional, so we pass empty sid
        return self._client.service.getAllProjects('')

    def get_project_description(self, project_id: str):
        """Returns name and description of project identified by ID. See also getAllProjects().

        Args:
            project_id (str): the project ID

        Returns:
            zeep.objects.projectInfo: project info with id, name and description
        """
        return self._client.service.getProjectDescription('', '', project_id)

    def get_user_role(self, sid: str, project_id: str):
        """Returns ePPNs plus Array of Roles of all members in the project.

        Caller must be member herself.

        Args:
            sid (str):  String, SessionID of user that wants to query for roles
            project_id (str): the project ID

        Returns:
            zeep.objects.getUserRoleResponse: ePPNs plus Array of Roles of all members in project
        """
        res = self._client.service.getUserRole(auth=sid, project=project_id)
        return res

    def get_ids(self, sid: str, name: str, mail: str, organisation: str):
        """Returns user records for a name or mail address.

        Args:
            sid (str): SessionID of user that wants to query for names
            name (str): Name
            mail (str): E-Mail Address
            organisation (str): Organisation

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            zeep.object.getIDsResponse: contains 0...n userDetails, which themselves have elements ePPN, name, mail,
                                        organisation, agreesearch, usersupplieddata
        """
        try:
            res = self._client.service.getIDs(
                auth=sid, name=name, mail=mail, organisation=organisation
            )
            return res
        except TransportError as error:
            message = 'Error searching for userIDs. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error

    def create_project(
        self, sid: str, name: str, description: str, default_owner_roles: Optional[bool] = True
    ) -> str:
        """Create a new project.

        Args:
            sid (str): TextGrid Session ID
            name (str): name of the project
            description (str): description for the project
            default_owner_roles (Optional[bool]): whether to assign the default roles to the owner
                                                  (editor, authority to delete). Defaults to True.

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            str: the project ID of the created project
        """
        try:
            project_id = self._client.service.createProject(
                auth=sid, name=name, description=description
            )
        except Fault as fault:
            message = 'Error creating project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault

        if default_owner_roles:
            eppn = self.get_eppn_for_sid(sid)
            self.add_editor_to_project(sid, project_id, eppn)
            self.add_admin_to_project(sid, project_id, eppn)

        return project_id

    def get_eppn_for_sid(self, sid: str) -> str:
        """Get the EPPN belonging to a sessionID.

        Args:
            sid (str): TextGrid Session ID

        Raises:
            TextgridAuthException: in case of transport exceptions

        Returns:
            str: the EPPN
        """
        try:
            eppn = self._extra_crud_client.service.getEPPN(auth=sid, secret='')
        except TransportError as error:
            message = 'Error getting eppn. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error
        return eppn

    def delete_project(self, sid: str, project_id: str) -> bool:
        """Delete a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            status = self._client.service.deleteProject(auth=sid, project=project_id)
        except Fault as fault:
            message = 'Error deleting project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault
        return status

    def add_admin_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the admin role in a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_ADMINISTRATOR)
        except TextgridAuthException as exception:
            raise exception

    def add_editor_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the editor role in a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_EDITOR)
        except TextgridAuthException as exception:
            raise exception

    def add_manager_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the manager role in a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_MANAGER)
        except TextgridAuthException as exception:
            raise exception

    def add_observer_to_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Give an user the observer role in a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._add_role_to_project(sid, project_id, eppn, TG_STANDARD_ROLE_OBSERVER)
        except TextgridAuthException as exception:
            raise exception

    def _add_role_to_project(self, sid: str, project_id: str, eppn: str, role: str) -> bool:
        rolename = role + ',' + project_id + ',Projekt-Teilnehmer'
        try:
            status = self._client.service.addMember(auth=sid, username=eppn, role=rolename)
        except Fault as fault:
            message = 'Error adding role to project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from fault
        return status

    def remove_admin_from_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Remove an users admin role in a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._remove_role_from_project(
                sid, project_id, eppn, TG_STANDARD_ROLE_ADMINISTRATOR
            )
        except TextgridAuthException as exception:
            raise exception

    def remove_editor_from_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Remove an users editor role from a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._remove_role_from_project(sid, project_id, eppn, TG_STANDARD_ROLE_EDITOR)
        except TextgridAuthException as exception:
            raise exception

    def remove_manager_from_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Remove an users manager role from a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._remove_role_from_project(sid, project_id, eppn, TG_STANDARD_ROLE_MANAGER)
        except TextgridAuthException as exception:
            raise exception

    def remove_observer_from_project(self, sid: str, project_id: str, eppn: str) -> bool:
        """Remove an users observer role from a project.

        Args:
            sid (str): TextGrid Session ID
            project_id (str): the project ID
            eppn (str): the eppn identifying the user

        Raises:
            TextgridAuthException: in case of tgauth faults

        Returns:
            bool: true in case of success
        """
        try:
            return self._remove_role_from_project(sid, project_id, eppn, TG_STANDARD_ROLE_OBSERVER)
        except TextgridAuthException as exception:
            raise exception

    def _remove_role_from_project(self, sid: str, project_id: str, eppn: str, role: str) -> bool:
        rolename = role + ',' + project_id + ',Projekt-Teilnehmer'
        try:
            status = self._client.service.deleteMember(auth=sid, username=eppn, role=rolename)
        except TransportError as error:
            message = 'Error removing role from project. Is your sessionID valid?'
            logger.warning(message)
            raise TextgridAuthException(message) from error
        return status


class TextgridAuthException(Exception):
    """Exception communicating with tgauth!"""
