import telebot, requests, json


#bot settings
API_KEY = "2011770125:AAEt0aMspKsSx67K-xC-AVF652MBZQWDPPM"
bot = telebot.TeleBot(API_KEY, num_threads=15)
#chat_id = "999523969"
chat_id = -1001742821948

def main():
    
    def empresa_rules(msg):
        if len(msg) == 1:
            bot.send_message(chat_id, f"Uso: /empresa <nome_da_empresa>")
            return False
        return True
    
    def area_rules(msg):
        if len(msg) == 1:
            bot.send_message(chat_id, f"Uso: /area <area_de_interesse>")
            return False
        return True
    
    def duvidas_rules(msg):
        if len(msg) != 1:
            bot.send_message(chat_id, f"Uso: /duvidas")
            return False
        return True
    
    def input_validation(msg, action):
        #empresa rules
        if (action == "empresa"):
            return empresa_rules(msg) 
        #area rules
        elif (action == "area"):
            return area_rules(msg)
        #duvidas rules 
        elif (action == "duvidas"):
            return duvidas_rules(msg)   
        return True
    
    def linkedin_request(terms):
        url = f"https://linkedin-jobs-search.p.rapidapi.com/"

        payload = {
            "search_terms": f"{terms}",
            "location": "30301",
            "page": "1",
            "fetch_full_text": "yes"
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com",
            "X-RapidAPI-Key": "48be49b171mshc147cb6ae473b41p1a5ce6jsn56ff4996e3a2"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        return response.json()    
    
    def expor_jobs(list_jobs):
        for job in list_jobs:
            text = f"""
            {job['job_title']}
            Company name: {job['company_name']}
            Location: {job['job_location']}
            URL: {job['linkedin_job_url_cleaned']}
            """
            bot.send_message(chat_id, text)
    
    @bot.message_handler(commands=["empresa"]) 
    def empresa(message):
        msg = list(filter(None, message.text.split(" ")))
        if (input_validation(msg, "empresa")):
            bot.send_message(chat_id, "Buscando ...")
            final = ""
            for i in range(1,len(msg)):
                final += msg[i]
            r = linkedin_request(final)
            expor_jobs(r)

    @bot.message_handler(commands=["area"]) 
    def area(message):
        msg = list(filter(None, message.text.split(" ")))
        if (input_validation(msg, "area")):
            bot.send_message(chat_id, "Buscando ...")
            final = ""
            for i in range(1,len(msg)):
                final += msg[i]
            r = linkedin_request(final)
            expor_jobs(r)
        
    @bot.message_handler(commands=["duvidas"]) 
    def duvidas(message):
        msg = list(filter(None, message.text.split(" ")))
        if (input_validation(msg, "duvidas")):
            bot.send_message(chat_id, "Espere alguns segundos que um de nossos atendentes de suporte irá contactá-lo")
        
    def validation(message):
        return True

    @bot.message_handler(func=validation)
    def resposta_padrao(message):
        bemvindo = "Bem vindo ao APP 'Os Desempregados'! :)"
        texto = f"""
        Escolha o comando para iniciar conosco:
        /empresa pesquisa por empregos em empresa específica
        /area pesquisa por empregos na área especificada
        /duvidas digite isso para ser direcionado ao nosso SAC
        """
        bot.reply_to(message, bemvindo)
        bot.send_message(chat_id, texto)

        
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)

if __name__ == '__main__':
    main()
