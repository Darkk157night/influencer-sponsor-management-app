from website import app,db,datetime
from flask import Flask,redirect,url_for,render_template,flash,request
from website.forms import loginForm,Register_companyForm,Register_influenceForm,Register_admin,create_campaign,AdRequestForm
from website.models import User,Sponsor,Influencer,Campaign,AdminFlag,AdRequest
from flask_login import login_user,login_required,current_user,logout_user

date_format = "%Y-%m-%d"

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login_page():
    form = loginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"success, logged in as: {attempted_user.username}",category='success')
            if attempted_user.role == 'admin':
                return redirect(url_for('website_page_admin'))
            elif attempted_user.role == 'sponsor':
                return redirect(url_for('website_page_sponsor'))
            else:
                return redirect(url_for('website_page_influencer'))
        else:
            flash('Username and password dont match',category='danger')
    return render_template('login.html',form=form)

@app.route('/register_influencer',methods=['POST','GET'])
def register_influencer_page():
    form = Register_influenceForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                    email_id = form.email_address.data,
                    password=form.password.data, 
                    role='influencer')
        db.session.add(user_to_create)
        db.session.commit()

        influencer = Influencer(user_id=user_to_create.id, 
                                name=form.name.data, 
                                email_id = user_to_create.email_id,
                                category=form.category.data, 
                                niche=form.niche.data, 
                                reach=form.reach.data)
        db.session.add(influencer)
        db.session.commit()
        
        login_user(user_to_create)
        flash(f'Account created successfully, you have logged in successfully as {user_to_create.username}',category='success')
        return redirect(url_for('website_page_influencer'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}')
    return render_template('register_influencer.html',form=form)

@app.route('/register_company',methods=['POST','GET'])
def register_company_page():
    form = Register_companyForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                    email_id = form.email_address.data,
                    password=form.password.data, 
                    role='sponsor')
        db.session.add(user_to_create)
        db.session.commit()

        sponsor = Sponsor(user_id=user_to_create.id, 
                          email_id = user_to_create.email_id,
                          name=form.name.data, 
                          industry=form.industry.data, 
                          budget=form.budget.data)
        db.session.add(sponsor)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully, you have logged in successfully as {user_to_create.username}',category='success')
        return redirect(url_for('website_page_sponsor'))
    if form.errors != {}: # no errors from the validations
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}')
    return render_template('register_company.html',form=form)

@app.route('/admin-create',methods=['POST','GET'])
def admin_create(): 
    form = Register_admin()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                    email_id = form.email_address.data,
                    password=form.password.data, 
                    role='admin')
        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)
        flash(f'Account created successfully, you have logged in successfully as {user_to_create.username}',category='success')
        return redirect(url_for('website_page_admin'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}')
    return render_template('admin_register.html',form=form)

@app.route('/Dashboard/Admin',methods=['POST','GET'])
@login_required
def website_page_admin():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home_page'))

    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()
    admin_flags = AdminFlag.query.all()
    
    return render_template('admin_dashboard.html', 
                           campaigns=campaigns, 
                           ad_requests=ad_requests,
                           admin_flags=admin_flags)

@app.route('/admin/campaign/<int:campaign_id>',methods=['POST','GET'])
@login_required
def admin_view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('admin_view_campaign.html', campaign=campaign)


@app.route('/admin/ad-request/<int:request_id>')
@login_required
def admin_view_ad_request(request_id):
    ad_request = AdRequest.query.get_or_404(request_id)
    return render_template('admin_view_ad_request.html', ad_request=ad_request)

@app.route('/admin/flag/<int:flag_id>')
@login_required
def admin_view_flag(flag_id):
    flag = AdminFlag.query.get_or_404(flag_id)
    return render_template('admin_view_flag.html', flag=flag)
    return render_template('admin_dashboard.html')

@app.route('/Dashboard/Sponsor',methods=['POST','GET'])
@login_required
def website_page_sponsor():
    current_sponsor = Sponsor.query.filter_by(id= current_user.id).first()
    campaigns= Campaign.query.filter_by(sponsor_id =current_user.id).all()
    return render_template('sponsor_dashboard.html',current_sponsor=current_sponsor,campaigns=campaigns)

@app.route('/Dashboard/Influencer',methods=['POST','GET'])
@login_required
def website_page_influencer():
    current_influencer = Influencer.query.filter_by(id=current_user.id).first()
    ad_requests = AdRequest.query.filter_by(influencer_id=current_user.id).all()
    return render_template('influencer_dashboard.html',current_influencer=current_influencer,ad_requests=ad_requests)

@app.route('/Dashboard/Sponsor/Create-Campaign',methods=['POST','GET'])
@login_required
def create_campaign_page():
    form = create_campaign()
    if form.validate_on_submit():
        campaign_to_create= Campaign(name= form.name.data,
                             sponsor_id = current_user.id,
                             description = form.description.data,
                             start_date=form.start_date.data,
                             end_date=form.end_date.data,
                             status = 'ongoing',
                             budget = form.budget.data,
                             visibility= form.visibility.data,
                             goals = form.goals.data)
        db.session.add(campaign_to_create)
        db.session.commit()
        return redirect(url_for('website_page_sponsor'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}')
    return render_template('campaign_create.html',form=form)

## Campaign update and delete
@app.route('/campaign/<int:campaign_id>')
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('view_campaign.html', campaign=campaign)

@login_required
@app.route('/campaign/<int:campaign_id>/update', methods=['POST','GET'])
def update_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    campaign.name = request.form['name']
    campaign.description = request.form['description']
    campaign.status = request.form['status']
    start_date_str = request.form['start_date']
    start_date = datetime.strptime(start_date_str, date_format).date()

    # Parse the end date
    end_date_str = request.form['end_date']
    end_date = datetime.strptime(end_date_str, date_format).date()
    campaign.visibility = request.form['visibility']
    
    db.session.commit()
    flash('Campaign updated successfully', 'success')
    return redirect(url_for('view_campaign', campaign_id=campaign.id))


@login_required
@app.route('/Admin/view-flags')
def admin_flag_view_page():
    flags = AdminFlag.query.all()
    return render_template('admin_view_flag.html',flag=flags)

@login_required
@app.route('/Ad-request-page',methods = ['POST','GET'])
def Ad_request_page():
    return render_template('ad_request_page.html')

@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully', 'success')
    if current_user.role == 'admin':
        return redirect(url_for('website_page_admin'))
    return redirect(url_for('website_page_sponsor'))


@app.route('/ad-request/new/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def new_ad_request(campaign_id):
    form = AdRequestForm()
    form.campaign_id.data = campaign_id
    form.influencer_id.data = current_user.id  # Assuming current_user is the influencer

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=form.influencer_id.data,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status=form.status.data
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad Request created successfully', 'success')
        return redirect(url_for('website_page_influencer')) 
    return render_template('ad_request_form.html', form=form)

@app.route('/Dashboard/Influencer/Campaigns-page',methods=['POST','GET'])
@login_required
def campaigns_page():
    title = request.args.get('title', '')
    category = request.args.get('category', '')  
    niche = request.args.get('niche', '')       

    # Build the query
    query = Campaign.query.filter_by(visibility='Public', status='ongoing')
    
    if title:
        query = query.filter(Campaign.name.ilike(f'%{title}%'))
    if category:
        query = query.filter(Campaign.category.ilike(f'%{category}%'))
    if niche:
        query = query.filter(Campaign.niche.ilike(f'%{niche}%'))
    
   
    campaigns = query.all()
    
    return render_template('campaigns_listing.html', campaigns=campaigns)


@app.route('/Dashboard/influencers-page')
@login_required
def influencer_list():
    # Get search parameters
    name = request.args.get('name', '')
    category = request.args.get('category', '')
    niche = request.args.get('niche', '')
    min_reach = request.args.get('min_reach', '')

    
    query = Influencer.query

    
    if name:
        query = query.filter(Influencer.name.ilike(f'%{name}%'))
    if category:
        query = query.filter(Influencer.category.ilike(f'%{category}%'))
    if niche:
        query = query.filter(Influencer.niche.ilike(f'%{niche}%'))
    if min_reach:
        query = query.filter(Influencer.reach >= int(min_reach))

    # Execute query and get results
    influencers = query.all()

    return render_template('influencer_listings.html',influencers=influencers)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out',category='info')
    return redirect(url_for('home_page'))



@app.route('/admin/flag-campaign', methods=['POST'])
@login_required
def admin_flag_campaign():
    campaign_id = request.form.get('campaign_id')
    reason = request.form.get('reason')

    if not campaign_id or not reason:
        flash('Campaign ID and reason are required to flag a campaign.', 'danger')
        return redirect(url_for('website_page_admin'))

    campaign = Campaign.query.get_or_404(campaign_id)
    user_id = current_user.id  

    
    campaign.status = 'Flagged'

    AdRequest.query.filter_by(campaign_id=campaign_id).delete()

    # Create a new flag entry
    new_flag = AdminFlag(user_id=user_id, campaign_id=campaign_id, reason=reason)
    db.session.add(new_flag)

    # Commit the changes to the database
    db.session.commit()

    flash('Campaign flagged successfully and all associated ad requests have been deleted.', 'success')
    return redirect(url_for('website_page_admin'))



@app.route('/admin/flag_campaign/<int:campaign_id>', methods=['GET'])
@login_required
def show_flag_form(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('flag_campaign.html', campaign=campaign)
