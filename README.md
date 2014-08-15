# Skiff

Wrapper for DigitalOcean's v2 API

![skiff](https://raw.githubusercontent.com/Shrugs/skiff/master/media/SkiffLogo.png)

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

    my_droplet = skiff.Droplet.create(name='hello.world', region='nyc1', size='512mb', image=5141286)
    >>> <hello.world (#2012974) nyc1 - Ubuntu 14.04 x64 - 512mb>

Alternatively, you can pass a dictionary containing these values.

#### Get
    # Get droplet by ID
    my_droplet = skiff.Droplet.get(id)
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

#### Get Droplet Snapshots
    my_droplet.snapshots()

#### Get Droplet Backups
    my_droplet.backups()

#### Get Droplet Actions
    my_droplet.actions()

#### Get Droplet Kernels
    my_droplet.kernels()

### Droplet Helper Methods

#### has_action_in_progress
Returns a boolean regarding whether or not the droplet is processing an action.

    my_droplet.has_action_in_progress()
    >>> False

### Actions

#### Get All Actions
Returns all actions for a token.

    skiff.Action.all()

#### Get Action by ID

    action_id = 28012139
    skiff.Action.get(action_id)
    >>> <destroy (#28012139) completed>

### Domains

#### Get All Domains
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

#### Get Specific Domain
    my_domain = skiff.Domain.get('example.com')
    my_domain = skiff.Domain.get(domain_id)

#### Delete/Destroy Domain
These are aliases for the same method.

    my_domain.delete()
    my_domain.destroy()

### Domain Records

#### Get Domain Records
    my_domain.records()
    >>>[<example.com - A (#348736) @ -> 123.456.789.123>,
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
    my_record = my_record.update('new_name')

See the [DigitalOcean v2 API Docs](https://developers.digitalocean.com/v2/#update-a-domain-record) for information on what `new_name` should be.

#### Delete/Destroy Domain Record
These are aliases for the same method.

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

#### Get Image by ID, Slug, or Search
    # Get by ID
    my_image_id = 3101580
    my_image = skiff.Image.get(my_image_id)
    # Or by slug
    ubuntu_slug = 'ubuntu1404'
    ubuntu_image = skiff.Image.get(ubuntu_slug)
    # Or by search (not very intelligent; useful for REPL use)
    ubuntu_image = skiff.Image.get('Ubuntu 13.10')

#### Delete/Destroy an Image
These are aliases for the same method.

    my_image.delete()
    my_image.destroy()

#### Update an Image
    name = 'my_new_image'
    my_image = my_image.update(name)

#### Transfer Image
    new_region = skiff.Region.get('nyc1')
    my_image.transfer(new_region)

Alternatively, simply pass the string 'nyc1'.

#### Get Image Actions
    my_image.actions()

#### Get Specific Image Action by ID
    action_id = 1234
    my_image.get_action(action_id)

### Keys

#### Get All Keys
    skiff.Key.all()

#### Get Specific Key by ID, Name or, Fingerprint
    # ID
    my_key = skiff.Key.get(1234)
    # Name
    my_key = skiff.Key.get('my public key')
    # Fingerprint
    my_key = skiff.Key.get('my:fi:ng:er:pr:in:t!')

#### Create New Key
    with open('~/.ssh/id_rsa.pub', 'r') as f:
        pub_key = f.read()
    my_key = skiff.Key.create(name='my public key', public_key=pub_key)

#### Update Key
    my_key = my_key.update('new public key name')

#### Delete/Destroy Key
These are aliases for the same method.

    my_key.delete()
    my_key.destroy()

### Regions

#### List All Regions
    skiff.Region.all()
    >>> [<New York 1 (nyc1)>,
    >>> <San Francisco 1 (sfo1)>,
    >>> <New York 2 (nyc2)>,
    >>> <Amsterdam 2 (ams2)>,
    >>> <Singapore 1 (sgp1)>]

#### Get Specific Region by Slug
There's probably not much benefit in getting a SkiffRegion instance rather than just passing the region slug string as a parameter.

    nyc1_region = skiff.Region.get('nyc1')

### Sizes

#### Get all Sizes
    skiff.Size.all()
    >>> [<512mb>, <1gb>, <2gb>, <4gb>, <8gb>, <16gb>, <32gb>, <48gb>, <64gb>]

### Get Specific Size
    # search, not intelligent
    small_size = skiff.Size.get('512')


## TODO

Make it so you can have multiple api wrappers at once that have different tokens, rather than the token being a 'global'.

## License 

MIT