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

"""gcloud dns project-info describe command."""

from googlecloudsdk.api_lib.dns import util
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.calliope import base
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Describe(base.DescribeCommand):
  """View Cloud DNS related information for a project.

  This command displays Cloud DNS related information for your project including
  quotas for various resources and operations.

  ## EXAMPLES

  To display Cloud DNS related information for your project, run:

    $ {command} my_project_id
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'dns_project', metavar='PROJECT_ID',
        help='The identifier for the project you want DNS related info for.')

  def Run(self, args):
    dns = apis.GetClientInstance('dns', 'v1')
    project_ref = resources.REGISTRY.Parse(
        args.dns_project, collection='dns.projects')

    return dns.projects.Get(
        dns.MESSAGES_MODULE.DnsProjectsGetRequest(
            project=project_ref.project))


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class DescribeBeta(base.DescribeCommand):
  """View Cloud DNS related information for a project.

  This command displays Cloud DNS related information for your project including
  quotas for various resources and operations.

  ## EXAMPLES

  To display Cloud DNS related information for your project, run:

    $ {command} my_project_id
  """

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'dns_project', metavar='PROJECT_ID',
        help='The identifier for the project you want DNS related info for.')

  def Run(self, args):
    dns = apis.GetClientInstance('dns', 'v1beta2')
    project_ref = util.GetRegistry('v1beta2').Parse(
        args.dns_project, collection='dns.projects')

    return dns.projects.Get(
        dns.MESSAGES_MODULE.DnsProjectsGetRequest(
            project=project_ref.project))
