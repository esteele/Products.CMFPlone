## Script (Python) "personalize"
##title=Personalization Handler.
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=portrait=None
from Products.CMFPlone import transaction_note
REQUEST=context.REQUEST
portrait_id='MyPortrait'
skinvar=context.portal_skins.getRequestVarname()

errors=context.validate_personalize()
if errors:
    edit_form=getattr(context, 'personalize_form')
    return edit_form(errors)
    
try:
    context.portal_registration.setProperties(REQUEST)
except: #CMF1.3 below
    member=context.portal_membership.getAuthenticatedMember()
    member.setProperties(REQUEST)
    
context.portal_skins.updateSkinCookie()
    
#if a portait file was upload put it in the /Members/XXXX/.personal/MyPortrait
if portrait and portrait.filename:
    personal=context.getPlonePersonalFolder()
    if not personal:
        home=context.portal_membership.getHomeFolder()
        home.manage_addProduct['CMFCore'].manage_addContent(type='Portal Folder', id='.personal')
        personal=getattr(home, '.personal')
    if not hasattr(personal, portrait_id):
        personal.invokeFactory(type_name='Image', id=portrait_id)
    portrait_obj=getattr(personal, portrait_id, None)
    portrait_obj.edit(file=portrait)

qs = '/personalize_form?portal_status_message=Member+changed.'
tmsg=context.portal_membership.getAuthenticatedMember().getUserName()+' personalized their settings.'
transaction_note(tmsg)
return REQUEST.RESPONSE.redirect(context.portal_url() + qs)
