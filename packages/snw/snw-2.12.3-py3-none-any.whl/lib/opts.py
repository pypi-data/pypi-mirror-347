#!/usr/bin/env python
# coding: utf-8

import client.launcher as launcher


def make_inter_subparser(parser):
    parser.add_argument('-s', '--service', help="service name")
    parser.add_argument('--storage_path', help='path to the remote storage', required=True)
    parser.add_argument('--file', help='path to the local file', required=True)
    parser.add_argument('--source_lang', help='Source lang of the file', required=True)
    parser.add_argument('--target_lang', help='Target lang of the file', required=False, default='')
    parser.add_argument(
        '--search_side',
        help='Search side to perform the intersection (default: "source")',
        choices=["source", "target"],
        required=False,
        default='source'
    )


def define_option():
    launcher.subparsers_map["docker"] = launcher.subparsers.add_parser('docker')
    launcher.subparsers_map["model"] = launcher.subparsers.add_parser('model')
    launcher.subparsers_map["vocab"] = launcher.subparsers.add_parser('vocab')
    launcher.subparsers_map["resource"] = launcher.subparsers.add_parser('resource')
    launcher.subparsers_map["user"] = launcher.subparsers.add_parser('user')
    launcher.subparsers_map["tag"] = launcher.subparsers.add_parser('tag')
    launcher.subparsers_map["auth"] = launcher.subparsers.add_parser('auth')
    launcher.subparsers_map["inter"] = launcher.subparsers.add_parser('intersection')

    launcher.subparsers_map["entity"] = launcher.subparsers.add_parser('entity')
    launcher.subparsers_map["permission"] = launcher.subparsers.add_parser('permission')
    launcher.subparsers_map["role"] = launcher.subparsers.add_parser('role')
    launcher.subparsers_map["group"] = launcher.subparsers.add_parser('group')
    launcher.subparsers_map["share"] = launcher.subparsers.add_parser('share')
    launcher.subparsers_map["monitoring"] = launcher.subparsers.add_parser('monitoring')

    subparsers_auth = launcher.subparsers_map["auth"].add_subparsers(help='sub-command help',
                                                                     dest='subcmd')
    subparsers_auth.required = True

    parser_login = subparsers_auth.add_parser('login',
                                              help='{login} login to systran-nmt-wizard')
    launcher.shortcut_map["login"] = ["auth", "login"]
    parser_login.add_argument('-u', '--user', help='user')

    parser_auth = subparsers_auth.add_parser('token', help='{auth} get auth token for other user '
                                                           '(super only)')
    launcher.shortcut_map["auth"] = ["auth", "token"]
    parser_auth.add_argument('-u', '--user', required=True, help='user')
    parser_auth.add_argument('--duration', type=int, help='specify duration of token ')
    parser_auth.add_argument('--persistent', action='store_true',
                             help='use persistent for generating persistent api keys')

    parser_revoke = subparsers_auth.add_parser('revoke',
                                               help='{revoke} revoke a token (super only)')
    launcher.shortcut_map["revoke"] = ["auth", "revoke"]
    parser_revoke.add_argument('-T', '--token', type=str, required=True, help='the token to revoke')

    parser_logout = subparsers_auth.add_parser('logout',
                                               help='{logout} revoke current credentials')
    launcher.shortcut_map["logout"] = ["auth", "logout"]

    subparsers_vocab = launcher.subparsers_map["vocab"].add_subparsers(help='sub-command help',
                                                                       dest='subcmd')
    subparsers_vocab.required = True

    parser_get_vocab = subparsers_vocab.add_parser('get', help='download the vocab')
    parser_get_vocab.add_argument('vocab', help='vocab')
    parser_get_vocab.add_argument('-f', '--file', help='path to the file of the vocab')
    parser_get_vocab.add_argument('-o', '--output', help='path to the output file of the vocab')

    parser_detail_vocab = subparsers_vocab.add_parser('detail', help='{cv} show the model contents')
    launcher.shortcut_map["cv"] = ["vocab", "detail"]
    parser_detail_vocab.add_argument('vocab')
    parser_detail_vocab.add_argument('-d', '--directory', help='the directory inside the vocab')

    subparsers_model = launcher.subparsers_map["model"].add_subparsers(help='sub-command help',
                                                                       dest='subcmd')
    subparsers_model.required = True

    parser_list_models = subparsers_model.add_parser('list',
                                                     help='{lm} list available models')
    launcher.shortcut_map["lm"] = ["model", "list"]
    parser_list_models.add_argument('-s', '--source', help='source language prefix')
    parser_list_models.add_argument('-t', '--target', help='target language prefix')
    parser_list_models.add_argument('-m', '--model', nargs='*', help='pattern search by regex')
    parser_list_models.add_argument('--tags', nargs="*", help='model tags')
    parser_list_models.add_argument('--skip_noscores', action='store_true',
                                    help='skip models without scores')
    parser_list_models.add_argument('--has_noscores', action='store_true',
                                    help='only display models with scores missing')
    parser_list_models.add_argument('--avg_scores', action='store_true',
                                    help='display model average scores')
    parser_list_models.add_argument('--quiet', '-q', action='store_true',
                                    help='only display matching model ids')
    parser_list_models.add_argument('--show_owner', '-so', action='store_true',
                                    help='display model owner')
    parser_list_models.add_argument('--show_domain', '-sd', action='store_true',
                                    help='display model domain')
    parser_list_models.add_argument('--count', action='store_true',
                                    help='only display count of models')
    parser_list_models.add_argument('--aggr', choices=['lp', 'model'],
                                    help='aggregate models by `lp` or `model`')
    parser_list_models.add_argument('--scores', nargs='*', default=None,
                                    help='testset patterns to display along with the model')
    parser_list_models.add_argument('--metric', '-M', default='BLEU',
                                    help='metric to display (default BLEU)')
    parser_list_models.add_argument('--show_pruned', action='store_true',
                                    help='display pruned and not pruned models')
    parser_list_models.add_argument('--only_show_pruned', action='store_true',
                                    help='only display pruned models')
    parser_list_models.add_argument('--only_show_released', action='store_true',
                                    help='only display released models')

    parser_get_model = subparsers_model.add_parser('get', help='download the model')
    parser_get_model.add_argument('model', help='model')
    parser_get_model.add_argument('-f', '--file', help='path to the file of the model')
    parser_get_model.add_argument('-o', '--output', help='path to the output file of the model')

    parser_detail_model = subparsers_model.add_parser('detail', help='{cm} show the model contents')
    launcher.shortcut_map["cm"] = ["model", "detail"]
    parser_detail_model.add_argument('model')
    parser_detail_model.add_argument('-d', '--directory', help='the directory inside the model')

    parser_delete_models = subparsers_model.add_parser('delete',
                                                       help='{dm} delete specific models')
    launcher.shortcut_map["dm"] = ["model", "delete"]
    parser_delete_models.add_argument('-s', '--source', help='source language', required=True)
    parser_delete_models.add_argument('-t', '--target', help='target language', required=True)
    parser_delete_models.add_argument('--recursive', action='store_true',
                                      help='recursive deletion of each model and its descendant')
    parser_delete_models.add_argument('--include_released', action='store_true',
                                      help='delete models, including released models')
    parser_delete_models.add_argument('-f', '--force', action='store_true',
                                      help='do not ask confirmation of the deletion')
    parser_delete_models.add_argument('-d', '--dryrun', action='store_true',
                                      help='just simulate deletion to show models impacted')
    parser_delete_models.add_argument('models', nargs='+', type=str, help='model names')

    parser_add_model = subparsers_model.add_parser('add', help='{am} upload a model')
    launcher.shortcut_map["am"] = ["model", "add"]
    parser_add_model.add_argument('-f', '--file', help='path to tgz archive containing the model',
                                  required=True)
    parser_add_model.add_argument('--ignore_parent', action='store_true',
                                  help='if model parent not in catalog, drop connection '
                                       'to parent_model')
    parser_add_model.add_argument('--compute_checksum', action='store_true',
                                  help='recompute checksum during upload process')
    parser_add_model.add_argument('--name', '-N', type=str,
                                  help='rename during upload process')

    parser_describe_model = subparsers_model.add_parser('describe',
                                                        help='describe a model')
    parser_describe_model.add_argument('model', help='model')
    parser_describe_model.add_argument('-lp', '--language_pair', help='Language pair of the sub_config to retrieve')

    parser_addtag_model = subparsers_model.add_parser('tagadd', help='add tag[s] to a model')
    parser_addtag_model.add_argument('-m', '--model', help='model', required=True)
    parser_addtag_model.add_argument('-t', '--tags', nargs='+', type=str, help='tag names',
                                     required=True)
    parser_adddel_model = subparsers_model.add_parser('tagdel', help='remove tag[s] from a model')
    parser_adddel_model.add_argument('-m', '--model', help='model', required=True)
    parser_adddel_model.add_argument('-t', '--tags', nargs='+', type=str, help='tag names',
                                     required=True)

    parser_share_model = subparsers_model.add_parser('share', help='share a model with an entity')
    launcher.shortcut_map["ms"] = ["model", "share"]
    parser_share_model.add_argument('-m', '--model', help='model', required=True)
    parser_share_model.add_argument('-e', '--entity_code', help='2-letters entity code', required=True)

    parser_removeshare_model = subparsers_model.add_parser('removeshare',
                                                           help='remove the share visibility '
                                                                'of a model for an entity')
    launcher.shortcut_map["mrs"] = ["model", "removeshare"]
    parser_removeshare_model.add_argument('-m', '--model', help='model', required=True)
    parser_removeshare_model.add_argument('-e', '--entity_code', help='2-letters entity code', required=True)

    parser_open_model = subparsers_model.add_parser('open', help='open a model with an entity')
    launcher.shortcut_map["mo"] = ["model", "open"]
    parser_open_model.add_argument('-m', '--model', help='model', required=True)
    parser_open_model.add_argument('-e', '--entity_code', help='2-letters entity code', required=True)

    parser_removeopen_model = subparsers_model.add_parser('removeopen',
                                                          help='remove the open visibility '
                                                               'of a model for an entity')
    launcher.shortcut_map["mro"] = ["model", "removeopen"]
    parser_removeopen_model.add_argument('-m', '--model', help='model', required=True)
    parser_removeopen_model.add_argument('-e', '--entity_code', help='2-letters entity code', required=True)

    parser_prune_model = subparsers_model.add_parser('prune', help='{pm} prune a model')
    launcher.shortcut_map["pm"] = ["model", "prune"]
    parser_prune_model.add_argument('model', help='model', )
    parser_prune_model.add_argument('--include_released', action='store_true',
                                    help='prune the specified model, even if the model has already been released')

    parser_declare_model = subparsers_model.add_parser('declare', help='Declare a model in the catalog')
    parser_declare_model.add_argument(
        'model',
        help='model name to declare',
    )
    parser_declare_model.add_argument(
        '-lp',
        '--language_pair',
        help='Language pair of the model',
        required=True
    )
    parser_declare_model.add_argument(
        '--llm',
        help='Original LLM model name',
    )
    parser_declare_model.add_argument(
        '-i',
        '--image',
        help='image full name',
    )

    subparsers_docker = launcher.subparsers_map["docker"].add_subparsers(help='sub-command help',
                                                                         dest='subcmd')
    subparsers_docker.required = True

    parser_list_dockers = subparsers_docker.add_parser('list',
                                                       help='{ld} list available dockers')
    launcher.shortcut_map["ld"] = ["docker", "list"]
    parser_list_dockers.add_argument('-d', '--docker', default="",
                                     help='restrict to specific docker')

    parser_add_docker = subparsers_docker.add_parser('add', help='{ad} add docker configs and '
                                                                 'schema to db')
    launcher.shortcut_map["ad"] = ["docker", "add"]
    parser_add_docker.add_argument('-i', '--image', required=True,
                                   help='image full name')
    parser_add_docker.add_argument('-c', '--configs', required=True,
                                   help='docker configs')
    parser_add_docker.add_argument('-s', '--schema', required=True,
                                   help='schema for docker configs')

    parser_describe_docker = subparsers_docker.add_parser('describe',
                                                          help='describe a docker image')
    parser_describe_docker.add_argument('docker', help='docker to describe')
    parser_describe_docker.add_argument('-c', '--config', help='name of the config', required=True)

    subparsers_resource = launcher.subparsers_map["resource"].add_subparsers(help='sub-command '
                                                                                  'help',
                                                                             dest='subcmd')
    subparsers_resource.required = True

    parser_list_resources = subparsers_resource.add_parser('list',
                                                           help='{lr} list available resources')
    launcher.shortcut_map["lr"] = ["resource", "list"]
    parser_list_resources.add_argument('-s', '--service', help="service name")
    parser_list_resources.add_argument('path', nargs='?', default=None, help='subpath')
    parser_list_resources.add_argument('--aggr', action='store_true',
                                       help='aggregate file by suffixes')

    parser_get_resources = subparsers_resource.add_parser(
        'get', help='{gr} download a file from given storage'
    )

    launcher.shortcut_map["gr"] = ["resource", "get"]
    parser_get_resources.add_argument('-s', '--service', help="service name")
    parser_get_resources.add_argument('--paths', nargs='*', help='path to the files', required=True)
    parser_get_resources.add_argument('--format', help='file format (txt, tmx, json, tsv, json-edition)')
    parser_get_resources.add_argument('--output_dir', help='output directory of the downloaded files')

    parser_add_resources = subparsers_resource.add_parser('upload', help='{ur} upload files to '
                                                                         'given storage')
    launcher.shortcut_map["ur"] = ["resource", "upload"]
    parser_add_resources.add_argument('-s', '--service', help="service name")
    parser_add_resources.add_argument('--files', nargs='*', help='path to the local files',
                                      required=True)
    parser_add_resources.add_argument('--storage_path', help='path to the remote storage', required=True)

    parser_add_resources = subparsers_resource.add_parser('edit', help='{er} edit files in a '
                                                                       'given storage')
    launcher.shortcut_map["er"] = ["resource", "edit"]
    parser_add_resources.add_argument('-s', '--service', help="service name")
    parser_add_resources.add_argument('--path', help='path to the local file',
                                      required=False)
    parser_add_resources.add_argument('--storage_path', help='path to the remote storage', required=True)
    parser_add_resources.add_argument('--properties', action='store_true', help='Edit properties instead of file')
    parser_add_resources.add_argument('--filename', help='New filename')
    parser_add_resources.add_argument('--license', help='License of the corpus')
    parser_add_resources.add_argument('--publisher', help='Publisher of the corpus')
    parser_add_resources.add_argument('--source', help='Source of the corpus')
    parser_add_resources.add_argument('--domain', help='Domain of the corpus')
    parser_add_resources.add_argument('--genre', help='Genre of the corpus')
    parser_add_resources.add_argument('--notes', help='Any notes on the corpus (as a json string)')

    subparsers_user = launcher.subparsers_map["user"].add_subparsers(help='sub-command help',
                                                                     dest='subcmd')
    subparsers_user.required = True
    parser_list_users = subparsers_user.add_parser('list',
                                                   help='{lu} list users')
    launcher.shortcut_map["lu"] = ["user", "list"]

    parser_who = subparsers_user.add_parser('whoami', help='{who} show current user info')
    launcher.shortcut_map["who"] = ["user", "whoami"]

    parser_add_user = subparsers_user.add_parser('add', help='{au} add user')
    launcher.shortcut_map["au"] = ["user", "add"]
    parser_add_user.add_argument('--first_name', help='first name', required=True)
    parser_add_user.add_argument('--last_name', help='last name', required=True)
    parser_add_user.add_argument('-e', '--email', help='user email', required=True)
    parser_add_user.add_argument('-p', '--password', help='user password', required=True)
    parser_add_user.add_argument('--user_code', help='3-letter user code', required=True)
    parser_add_user.add_argument('--entity', help='entity id/name/code', required=True)
    parser_add_user.add_argument('--roles', nargs='*', help='roles')
    parser_add_user.add_argument('--groups', nargs='*', help='groups')

    parser_mod_user = subparsers_user.add_parser('modify', help='{mu} change user parameters')
    launcher.shortcut_map["mu"] = ["user", "modify"]
    parser_mod_user.add_argument('-u', '--user', help='user id/email/code', required=True)
    parser_mod_user.add_argument('--first_name', help='first name')
    parser_mod_user.add_argument('--last_name', help='last name')
    parser_mod_user.add_argument('-p', '--password', help='password')
    parser_mod_user.add_argument('--roles', nargs='*', help='roles')
    parser_mod_user.add_argument('--groups', nargs='*', help='groups')

    parser_del_user = subparsers_user.add_parser('delete', help='{du} remove user')
    launcher.shortcut_map["du"] = ["user", "delete"]
    parser_del_user.add_argument('-u', '--user', help='user id/email/code', required=True)

    parser_pwd_user = subparsers_user.add_parser('password', help='{password} change password')
    launcher.shortcut_map["password"] = ["user", "password"]
    parser_pwd_user.add_argument('-p', '--password', help='password', required=True)

    subparsers_tag = launcher.subparsers_map["tag"].add_subparsers(help='sub-command help',
                                                                   dest='subcmd')
    subparsers_tag.required = True
    parser_list_tags = subparsers_tag.add_parser('list', help='list tags')
    parser_add_tag = subparsers_tag.add_parser('add', help='add tag')
    parser_add_tag.add_argument('name', help='tag name')
    parser_detail_tag = subparsers_tag.add_parser('detail', help='show tag detail')
    parser_detail_tag.add_argument('name', help='tag name')
    parser_del_tag = subparsers_tag.add_parser('delete', help='remove tag')
    parser_del_tag.add_argument('name', help='tag name')
    parser_modify_tag = subparsers_tag.add_parser('modify', help='update tag name')
    parser_modify_tag.add_argument('name', help='current tag name')
    parser_modify_tag.add_argument('-n', '--newname', help='new tag name', required=True)

    parser_change_tasks = launcher.subparsers_tasks.add_parser('change',
                                                               help='{ct} change queued task')
    launcher.shortcut_map["ct"] = ["task", "change"]
    parser_change_tasks.add_argument('-p', '--prefix',
                                     help='prefix for the tasks to change')
    parser_change_tasks.add_argument('-P', '--priority', type=int,
                                     help='task priority - highest better')
    parser_change_tasks.add_argument('-Pr', '--priority_rand', type=int, default=0,
                                     help='for each task add this random number to priority')
    parser_change_tasks.add_argument('-s', '--service',
                                     help="service name")
    parser_change_tasks.add_argument('-g', '--gpus',
                                     help="number of gpus", type=int)
    parser_change_tasks.add_argument('-c', '--cpus',
                                     help="number of cpus", type=int)
    parser_change_tasks.add_argument('task_ids', nargs='*',
                                     help="task identifiers")

    launcher.parser_launch.add_argument('-N', '--no_test_trans', action='store_true',
                                        help="disable automatic test file translations")
    launcher.parser_launch.add_argument('--novalidschema', '--no_valid_schema', action='store_true',
                                        help='skip config validation')
    launcher.parser_launch.add_argument('--not_patch_envvar', action='store_true',
                                        help='do not auto patch storage environment variables')
    launcher.parser_launch.add_argument('--upgrade', choices=['auto', 'none', 'force'],
                                        default='auto',
                                        help='choice to upgrade when later docker image available:'
                                             ' `auto`(interactive), `none`, `force`')

    launcher.parser_exec.add_argument('--not_patch_envvar', action='store_true',
                                      help='do not auto patch storage environment variables')

    parser_config_service = launcher.subparsers_service.add_parser('config',
                                                                   help='configure a service')
    parser_config_service.add_argument('action',
                                       help="command list, set, get, del, select")
    parser_config_service.add_argument('-s', '--service', required=True,
                                       help="service name")
    parser_config_service.add_argument('-cn', '--configname',
                                       help="configuration name")
    parser_config_service.add_argument('-c', '--config',
                                       help="configuration file (for `set` only)")
    launcher.shortcut_map["listconfig"] = ["service", "config", "list"]
    launcher.shortcut_map["setconfig"] = ["service", "config", "set"]
    launcher.shortcut_map["getconfig"] = ["service", "config", "get"]
    launcher.shortcut_map["delconfig"] = ["service", "config", "del"]
    launcher.shortcut_map["selectconfig"] = ["service", "config", "select"]

    parser_disable_service = launcher.subparsers_service.add_parser('disable',
                                                                    help='disable a resource')
    parser_disable_service.add_argument('-r', '--resource', required=True,
                                        help="name of the resource")
    parser_disable_service.add_argument('-s', '--service', required=True,
                                        help="service name")
    parser_disable_service.add_argument('-m', '--message', required=True,
                                        help="add disabling message")

    parser_enable_service = launcher.subparsers_service.add_parser('enable',
                                                                   help='enable a resource')
    parser_enable_service.add_argument('-s', '--service', required=True,
                                       help="service name")
    parser_enable_service.add_argument('-r', '--resource', required=True,
                                       help="name of the resource")

    parser_stop_service = launcher.subparsers_service.add_parser('stop', help='stop a pool worker')
    parser_stop_service.add_argument('-s', '--service', help="service name", required=True)

    parser_restart_service = launcher.subparsers_service.add_parser('restart',
                                                                    help='restart a pool worker')
    parser_restart_service.add_argument('-s', '--service', help="service name", required=True)

    subparsers_entity = launcher.subparsers_map["entity"].add_subparsers(help='sub-command help',
                                                                         dest='subcmd')
    subparsers_entity.required = True
    parser_list_entities = subparsers_entity.add_parser('list',
                                                        help='list entities')
    parser_list_entities.add_argument('-a', '--all', action='store_true',
                                      help='show all entity (include disabled entities)')

    parser_add_entity = subparsers_entity.add_parser('add',
                                                     help='add a new entity')
    parser_add_entity.add_argument('--entity_code', help='2-letter entity code', required=True)
    parser_add_entity.add_argument('--name', help='entity name', required=True)
    parser_add_entity.add_argument('-e', '--email', help='email', required=True)
    parser_add_entity.add_argument('--tel', help='contact telephone')
    parser_add_entity.add_argument('--address', help='address of entity')
    parser_add_entity.add_argument('--description', help='description of entity')
    parser_modify_entity = subparsers_entity.add_parser('modify',
                                                        help='modify an entity')
    parser_modify_entity.add_argument('--entity', help='entity name/id/code', required=True)
    parser_modify_entity.add_argument('--name', help='new entity name')
    parser_modify_entity.add_argument('-e', '--email', help='email')
    parser_modify_entity.add_argument('--tel', help='entity telephone')
    parser_modify_entity.add_argument('--address', help='address of entity')
    parser_modify_entity.add_argument('--description', help='description of entity')

    # TODO implement it on server side
    # parser_delete_entity = subparsers_entity.add_parser('delete', help='delete an entity')
    # parser_delete_entity.add_argument('--entity', help='entity name/id/code', required=True)

    parser_disable_entity = subparsers_entity.add_parser('disable', help='disable an entity')
    parser_disable_entity.add_argument('--entity', help='entity name/id/code', required=True)

    parser_enable_entity = subparsers_entity.add_parser('enable', help='enable an entity')
    parser_enable_entity.add_argument('--entity', help='entity name/id/code', required=True)

    subparsers_role = launcher.subparsers_map["role"].add_subparsers(help='sub-command help',
                                                                     dest='subcmd')
    subparsers_role.required = True
    parser_list_roles = subparsers_role.add_parser('list',
                                                   help='list roles')
    parser_add_role = subparsers_role.add_parser('add',
                                                 help='add a new role for an entity')
    parser_add_role.add_argument('--name', help='role name', required=True)
    parser_add_role.add_argument('--entity', help='entity id/code/name', required=True)
    parser_add_role.add_argument('--permissions', help='permissions (possible prefix by '
                                                       'entity code) associated to the role',
                                 nargs='+', type=str)
    parser_modify_role = subparsers_role.add_parser('modify',
                                                    help='modify a role for an entity')
    parser_modify_role.add_argument('--role', help='role name or id', required=True)
    parser_modify_role.add_argument('--name', help='role new name')
    parser_modify_role.add_argument('--permissions', help='permissions (possible prefix by '
                                                          'entity code) associated to the role',
                                    nargs='*', type=str)
    parser_delete_role = subparsers_role.add_parser('delete',
                                                    help='modify a role for an entity')
    parser_delete_role.add_argument('--role', help='role name or id', required=True)

    subparsers_share = launcher.subparsers_map["share"].add_subparsers(help='sub-command help',
                                                                       dest='subcmd')
    parser_add_share = subparsers_share.add_parser('add',
                                                   help='share a role from an entity to '
                                                        'another entity')
    parser_add_share.add_argument('--roles', help='role name or id', nargs="+", required=True)
    parser_add_share.add_argument('--src_entity', help='source entity', required=True)
    parser_add_share.add_argument('--dest_entity', help='destination entity', required=True)

    parser_delete_share = subparsers_share.add_parser('delete',
                                                      help='remove a shared role from an entity to '
                                                           'another entity')
    parser_delete_share.add_argument('--roles', help='role name or id', nargs="+", required=True)
    parser_delete_share.add_argument('--src_entity', help='source entity', required=True)
    parser_delete_share.add_argument('--dest_entity', help='destination entity', required=True)

    subparsers_group = launcher.subparsers_map["group"].add_subparsers(help='sub-command help',
                                                                       dest='subcmd')
    subparsers_group.required = True
    parser_list_groups = subparsers_group.add_parser('list',
                                                     help='list groups')
    parser_add_group = subparsers_group.add_parser('add',
                                                   help='add a new group for an entity')
    parser_add_group.add_argument('--name', help='group name', required=True)
    parser_add_group.add_argument('--entity', type=str, help='entity id/code/name')
    parser_add_group.add_argument('--users', nargs='*', help='users')
    parser_add_group.add_argument('--roles', nargs='*', help='roles')

    parser_modify_group = subparsers_group.add_parser('modify',
                                                      help='modify a group for an entity')
    parser_modify_group.add_argument('--group', help='group name or id', required=True)
    parser_modify_group.add_argument('--name', help='group new name')
    parser_modify_group.add_argument('--users', nargs='*', help='users')
    parser_modify_group.add_argument('--roles', nargs='*', help='roles')

    parser_delete_group = subparsers_group.add_parser('delete',
                                                      help='modify a group for an entity')
    parser_delete_group.add_argument('--group', help='group name or id', required=True)

    subparsers_permission = launcher.subparsers_map["permission"].add_subparsers(help='sub-command '
                                                                                      'help',
                                                                                 dest='subcmd')
    subparsers_permission.required = True
    parser_list_permissions = subparsers_permission.add_parser('list',
                                                               help='list permissions')

    subparsers_inter = launcher.subparsers_map["inter"].add_subparsers(
        help="sub-command help", dest="subcmd"
    )
    subparsers_inter.required = True

    parser_inter_exact = subparsers_inter.add_parser("exact", help="Exact intersection")
    launcher.shortcut_map["int-ex"] = ["intersection", "exact"]
    make_inter_subparser(parser_inter_exact)

    parser_inter_partial = subparsers_inter.add_parser(
        "partial", help="Partial intersection"
    )
    launcher.shortcut_map["int-pr"] = ["intersection", "partial"]
    make_inter_subparser(parser_inter_partial)

    parser_inter_nearmatch = subparsers_inter.add_parser(
        "nearmatch", help="Near-match intersection"
    )
    launcher.shortcut_map["int-nm"] = ["intersection", "nearmatch"]
    make_inter_subparser(parser_inter_nearmatch)

    parser_inter_nearpartial = subparsers_inter.add_parser(
        "nearpartial", help="Partial + near-match intersection"
    )
    launcher.shortcut_map["int-np"] = ["intersection", "nearpartial"]
    make_inter_subparser(parser_inter_nearpartial)
