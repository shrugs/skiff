# Skiff

Wrapper for DigitalOCean's v2 API

## Installation
    pip install skiff

## Basic Usage
    import skiff
    skiff.token("<my_token>")
    droplets = skiff.Droplet.all()
    >>> [<cond.in (#267357) nyc1 - Ubuntu 12.10 x64 - 512mb>,
    >>> <hey.github (#2012972) nyc1 - Ubuntu 13.10 x32 - 512mb>,
    >>> <hello.world (#2012974) nyc1 - Ubuntu 13.10 x32 - 512mb>]

## API

### Droplets

#### Create

    my_droplet = skiff.Droplet.create(name='hello.world', region='nyc1', size='512mb', image=3101580)
    >>> <hello.world (#2012974) nyc1 - Ubuntu 13.10 x32 - 512mb>

Alternatively, you can pass a dictionary containing these values.

#### Get
    # Get droplet by ID
    my_droplet = skill.Droplet.get(id)
    # Get droplet by Name (not intelligent)
    my_droplet = skiff.Droplet.get('hello.world')

#### Destroy
    my_droplet.destroy()

#### Rename
    my_droplet.rename('new.name')

#### Reboot
    my_droplet.reboot()
    my_droplet.restart()

#### Shutdown
    my_droplet.shutdown()

#### Power Off
    my_droplet.power_off()

#### Power On
    my_droplet.power_on()

#### Power Cycle
    my_droplet.power_cycle()

#### Resize
    # Get size via search
    some_size = skiff.Size.get('512')
    >>> <512mb>
    my_droplet.resize(some_size)

Alternatively, simply pass in the string `'512mb'`.

#### Rebuild
    ubuntu_image = skiff.Image.get('Ubuntu 13.10')
    my_droplet.rebuild(ubuntu_image)

#### Restore
    # Default to current Image
    my_droplet.restore()
    # Specify Image
    ubuntu_image = skiff.Image.get('Ubuntu 13.10')
    my_droplet.restore(ubuntu_image)

#### Password Reset
    my_droplet.password_reset()
    my_droplet.reset_password()

#### Change Kernel
    new_kernel = my_droplet.kernels()[10]
    my_droplet.change_kernel(new_kernel)

Alternatively, simply pass the kernel's ID.

#### Enable IPv6
    my_droplet.enable_ipv6()

#### Disable Backups
    my_droplet.disable_backups()

#### Enable Private Networking
    my_droplet.enable_private_networking()

#### Snapshots
    my_droplet.snapshots()

#### Backups
    my_droplet.backups()

#### Actions
    my_droplet.actions()

#### Kernels
    my_droplet.kernels()


### Actions

#### All Actions
Returns all actions for a token.

    skiff.Action.all()

#### Retrieve Action by ID

    action_id = 28012139
    skiff.Action.get(action_id)
    >>> <destroy (#28012139) completed>

### Domains

#### All Domains
    skiff.Domain.all()
    >>> [<blog.cond.in>,
    >>> <matt.cond.in>,
    >>> <example.com>,
    >>> <example2.com>]

#### Create Domain
    # easy, defaulting to fist ipv4 network's public ip
    my_domain = my_droplet.create_domain('example.com')

    # or more manually
    my_domain = skiff.Domain.create(name='example.com', ip_address=my_droplet.v4[0].ip_address)

#### Get Domain
    my_domain = skiff.Domain.get('example.com')
    my_domain = skiff.Domain.get(domain_id)

#### Delete/Destroy Domain
    my_domain.delete()
    my_domain.destroy()

### Domain Records

#### Get Domain Records
    my_domain.records()
    >>>[<example.com - A (#348736) @ -> some.ip.addr.ess>,
    >>> <example.com - CNAME (#348740) www -> @>,
    >>> <example.com - NS (#348737)  -> NS1.DIGITALOCEAN.COM.>,
    >>> <example.com - NS (#348738)  -> NS2.DIGITALOCEAN.COM.>,
    >>> <example.com - NS (#348739)  -> NS3.DIGITALOCEAN.COM.>]

#### Create Domain Records
    my_domain.create_record(type='CNAME', name='www', data='@')

See the [DigitalOcean v2 API Docs](https://developers.digitalocean.com/v2/#create-a-new-domain-record) for more options.

#### Get Domain Record by ID
    my_record_id = 1234
    my_record = my_domain.get_record(my_record_id)

#### Update Domain Record
    my_record.update('new_name')

See the [DigitalOcean v2 API Docs](https://developers.digitalocean.com/v2/#update-a-domain-record) for information on what `new_name` should be.

#### Delete/Destroy Domain Record
    my_record.delete()
    my_record.destroy()

### Images

#### List All Images
    skiff.Image.all()
    >>> [<CentOS 5.8 x64 (#1601) CentOS>,
    >>> <CentOS 5.8 x32 (#1602) CentOS>,
    >>> ...........
    >>> <CentOS 6.5 x64 (#3448641) CentOS>,
    >>> <Debian 6.0 x64 (#12573) Debian>]

#### Get Image by ID or Slug
    # Get by ID
    my_image_id = 3101580
    my_image = skiff.Image.get(my_image_id)
    # Or by slug
    ubuntu_slug = 'ubuntu1404'
    ubuntu_image = skiff.Image.get(ubuntu_slug)

#### Delete/Destroy an Image
    my_image.delete()
    my_image.destroy()

#### Update and Image
    name = 'my_new_image'
    my_image.update(name)

#### Transfer Image
    new_region = skiff.Region.get('nyc1')
    my_image.transfer(new_region)

#### Get Image Actions
    my_image.actions()

#### Get Specific Image Action by ID
    action_id = 1234
    my_image.get_action(action_id)


## TODO

Make it so you can have multiple api wrappers at once that have different tokens, rather than the token being a 'global'.

## License 

MIT