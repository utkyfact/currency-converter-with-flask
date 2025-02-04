from flask import Flask, render_template, request, redirect, url_for, flash
from currency_converter import CurrencyConverter, RateNotFoundError


app = Flask(__name__)
app.secret_key = 'gizli_anahtar_123'


@app.route('/', methods=["GET","POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency'].upper()
            to_currency = request.form['to_currency'].upper()

            c = CurrencyConverter()
            
            if from_currency not in c.currencies or to_currency not in c.currencies:
                flash('Geçersiz para birimi! Lütfen geçerli bir para birimi giriniz.', 'error')
                return render_template('index.html', 
                                    amount=amount,
                                    from_currency=from_currency,
                                    to_currency=to_currency)

            result = c.convert(amount, from_currency, to_currency)
            
            return render_template('index.html', 
                                result=result, 
                                amount=amount,
                                from_currency=from_currency,
                                to_currency=to_currency)

        except RateNotFoundError:
            flash('Dönüşüm oranı bulunamadı! Lütfen geçerli para birimleri giriniz.', 'error')
            return render_template('index.html')
        except ValueError:
            flash('Lütfen geçerli bir miktar giriniz!', 'error')
            return render_template('index.html')

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

