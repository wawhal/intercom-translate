# intercom-translate

## What is it?

Intercom is a customer support platform that allows businesses to chat with prospective and existing customers within their app, on their website, through social media, or via email.

As awesome as intercom is, every company almost always faces the problem of supporting customers worldwide due to the language barrier. Solving this problem is this webhook that receives message in any language, and replies back in the same language.

## How it works?

### Workflow

Lets consider a hypothetical situation where CompanyX is using Intercom and has enabled this webhook. Say I am a French guy who knows French and only French while the support team at CompanyX knows only English. So my interaction with CompanyX goes as follows:

1. I write my query as "Comment utiliser votre produit" which means "How to use your product".
2. The support team at CompanyX gets this message "Comment utiliser votre produit" and also an internal note which contains the translation i.e "How to use your product" and the language code i.e. "fr".
3. Now the support team knows only english. So they write an internal note saying "/translate fr" where `/translate` is the keyword for translating, `fr` is the language code.
4. Once the translate mode is on, the support team writes an internal note saying "Please read our documentation."
4. I will get a reply from the support team saying "Veuillez lire notre documentation".

Smoothe. Isn't it?

### Internal Implementation

1. When the user sends a message, it is sent to the webhook by intercom.
2. The webhook translates the message to English using the Google Translation API and writes it as an internal note to the team. (No action is taken if the source language is English)
3. Now when the the team member writes an internal note using `/translate <language-code>`, the conversation ID and the language code is stored in the database.
4. Now when a team member writes an internal note in a conversation, if there is a language code associated with that conversation in the database, it is translated to that lanuage and sent to the user.
5. When the team member types `/translate off`, the entry is deleted from the database.

## What does it use?

1. [Hasura](https://hasura.io)
2. [Intercom API](https://developers.intercom.com/v2.0/reference)
3. [Google Cloud Translation API](https://cloud.google.com/translate/docs/)

## How do I use it in my intercom workspace?

1. Install [hasura CLI](https://docs.hasura.io/0.15/manual/install-hasura-cli.html)

2. Get the project and `cd` into it.

```
$ hasura quickstart rishi/intercom-translate
```
3. Choose a default intercom admin to send translated messages. Find the [admin](https://developers.intercom.com/v2.0/reference#admins) id of that admin. Add it to your project secrets.

```
$ hasura secret update chatbot.admin.id <admin_id>
```

4. Create a webhook for your intercom workspace. Check the following three checkboxes:
  - New message from a user or lead
  - Reply from a user or lead
  - Note added to a conversation

  Add the URL as `https://bot.<cluster-name>.hasura-app.io/bot`. Run `hasura cluster status` to find your cluster name.

5. Create an [access token](https://developers.intercom.com/v2.0/reference#personal-access-tokens-1) for your intercom workspace and add it to secrets as well.

```
$ hasura secret update chatbot.access.token <access_token>
```

6. Create a project on [Google Cloud Platform](https://console.cloud.google.com/home/dashboard) (it is free). Get the [API key](https://support.google.com/cloud/answer/6158862?hl=en) and add it to your project secrets.

```
$ hasura secret update translate.api.key <api_key>
```

7. Enable the [Google Cloud Translation API](https://console.cloud.google.com/apis/library/translate.googleapis.com) for your project on Google Cloud Platform.

8. Finally, deploy the webhook using git push. Run these commands from the project directory.

```
$ git add .
$ git commit -m "First commit"
$ git push hasura master
```

   It is all set. You can check the translation functionality in action in your intercom workspace.

## How to build on top of this?

This webhook is written in Python using the Flask framework. The source code lies in `microservices/bot/app/src` directory. `server.py` is where you want to start modifying the code.

If you are using any extra python packages, just add them to `microservices/bot/app/src/requirements.txt` and they will be "pip installed" during the Docker build.

## Support

If you happen to get stuck anywhere, please mail me at rishichandrawawhal@gmail.com. Alternatively, if you find a bug, you can raise an issue [here](https://github.com/wawhal/intercom-translate/issues).
