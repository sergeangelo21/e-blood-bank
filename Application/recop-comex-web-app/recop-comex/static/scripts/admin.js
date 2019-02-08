var f = []

function check_pass()
{

    pass = document.getElementById('password')
    confirm = document.getElementById('password_confirm')

    if (pass.value!=confirm.value)
    {
        alert('Passwords did not match.')
        return false
    }
    else
    {
        return true
    }
}

function event_pages(value)
{

	info = document.getElementById('info_div')
	tracker = document.getElementById('tracker_div')
	participant = document.getElementById('participant_div')

	if (value=='info')
	{

		info.className='container'
		tracker.className='container hidden'
		participant.className='container hidden'

	}
	else if (value=='tracker')
	{

		tracker.className='container'
		info.className='container hidden'
		participant.className='container hidden'

	}
	else
	{

		participant.className='container'
		info.className='container hidden'
		tracker.className='container hidden'

	}

}

function filter(value)
{

	sender = document.getElementById(value)

	if (sender.checked==true)
	{
		f.push(value)
	}
	else
	{
		f.splice( f.indexOf(value), 1 );
	}

	var tbody = document.getElementsByTagName('tbody')

	if (f.length!=0)
		{
			for (ctr=0; ctr<=f.length-1; ctr++)
			{
				for (ctr2=0; ctr2<=tbody.length-1; ctr2++)
				{
						if(tbody[ctr2].id.indexOf(f[ctr].toString()+'_') && tbody[ctr2].name!="Y")
						{
							tbody[ctr2].style.display="none"
							tbody[ctr2].name="Y"
						}
						else
						{ 
							tbody[ctr2].style.display=""
						}
				}
				for (ctr2=0; ctr2<=tbody.length-1; ctr2++)
				{
					tbody.name=""
				}
			}
		}
		else
		{
			for (ctr2=0; ctr2<=tbody.length; ctr2++)
			{
				tbody[ctr2].style.display=""
			}
		}
	}