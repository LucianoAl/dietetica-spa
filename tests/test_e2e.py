from playwright.sync_api import sync_playwright

def test_flujo_compra():
    with sync_playwright() as p:
        # Abre el navegador en segundo plano
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Entra a tu página web local
        page.goto("http://127.0.0.1:5000/")
        
        # Verifica que los productos cargaron
        page.wait_for_selector(".card")
        
        # Hace clic en el botón añadir del primer producto
        page.click(".btn-add >> nth=0")
        
        # Espera a que el contador de carrito cambie de 0 a 1
        page.wait_for_function("document.querySelector('#cart-count').innerText !== '0'")
        
        # Confirma que el total sea mayor a 0
        total_text = page.locator("#total-flotante").inner_text()
        assert total_text != "0"
        
        print("-> Test E2E: Flujo de compra validado correctamente.")
        browser.close()

if __name__ == "__main__":
    test_flujo_compra()