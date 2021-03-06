# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for deleting vpn tunnels."""
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.vpn_tunnels import flags


class Delete(base.DeleteCommand):
  """Delete vpn tunnels.

  *{command}* deletes one or more Google Compute Engine vpn tunnels.
  """

  VPN_TUNNEL_ARG = None

  @staticmethod
  def Args(parser):
    Delete.VPN_TUNNEL_ARG = flags.VpnTunnelArgument(plural=True)
    Delete.VPN_TUNNEL_ARG.AddArgument(parser, operation_type='delete')
    parser.display_info.AddCacheUpdater(flags.VpnTunnelsCompleter)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    vpn_tunnel_refs = Delete.VPN_TUNNEL_ARG.ResolveAsResource(
        args,
        holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(client))

    utils.PromptForDeletion(vpn_tunnel_refs, 'region')

    requests = []
    for vpn_tunnel_ref in vpn_tunnel_refs:
      requests.append((client.apitools_client.vpnTunnels, 'Delete',
                       client.messages.ComputeVpnTunnelsDeleteRequest(
                           **vpn_tunnel_ref.AsDict())))

    return client.MakeRequests(requests)
