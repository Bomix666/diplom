// script.js
document.addEventListener("DOMContentLoaded", function() {
  const links = document.querySelectorAll(".nav-link"); // Селектим все ссылки
  const sections = document.querySelectorAll("section"); // Селектим все секции

  links.forEach(link => {
      link.addEventListener("click", function(e) {
          e.preventDefault(); // Отменяем стандартное поведение ссылки (перезагрузка страницы)

          // Скрываем все секции
          sections.forEach(section => {
              section.classList.add("hidden");
          });

          // Убираем активный класс у всех ссылок
          links.forEach(link => {
              link.classList.remove("text-gray-900");
              link.classList.add("text-white");
          });

          // Отображаем соответствующую секцию
          const targetSection = document.querySelector(link.getAttribute("href"));
          targetSection.classList.remove("hidden");

          // Добавляем активный класс для текущей вкладки
          link.classList.remove("text-white");
          link.classList.add("text-gray-900");
      });
  });
});

// Инициализация Three.js
let scene, camera, renderer, particles;

function initThree() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById('bg-canvas'),
        alpha: true
    });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // Создаем частицы
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1000;
    const posArray = new Float32Array(particlesCount * 3);

    for(let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 5;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.005,
        color: '#3B82F6',
        transparent: true,
        opacity: 0.8
    });

    particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    camera.position.z = 2;
}

// Анимация частиц
function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.001;
    particles.rotation.x += 0.0005;
    renderer.render(scene, camera);
}

// Обработка изменения размера окна
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Управление модальным окном
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('hidden');
    gsap.from(modal.children[0], {
        y: -50,
        opacity: 0,
        duration: 0.3
    });
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    gsap.to(modal.children[0], {
        y: -50,
        opacity: 0,
        duration: 0.3,
        onComplete: () => {
            modal.classList.add('hidden');
        }
    });
}

// Переключение между входом и регистрацией
function toggleAuthMode() {
    const title = document.getElementById('authTitle');
    const toggle = document.getElementById('authToggle');
    const loginFields = document.querySelector('.login-fields');
    const registerFields = document.querySelector('.register-fields');
    const submitButton = document.querySelector('#authForm button[type="submit"]');

    if (title.textContent === 'Вход') {
        title.textContent = 'Регистрация';
        toggle.textContent = 'Уже есть аккаунт?';
        submitButton.textContent = 'Зарегистрироваться';
        gsap.to(loginFields, { opacity: 0, display: 'none', duration: 0.3 });
        gsap.to(registerFields, { opacity: 1, display: 'block', duration: 0.3, delay: 0.3 });
    } else {
        title.textContent = 'Вход';
        toggle.textContent = 'Создать аккаунт';
        submitButton.textContent = 'Войти';
        gsap.to(registerFields, { opacity: 0, display: 'none', duration: 0.3 });
        gsap.to(loginFields, { opacity: 1, display: 'block', duration: 0.3, delay: 0.3 });
    }
}

// Показ вкладок
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });

    const targetTab = document.getElementById(tabId);
    targetTab.classList.remove('hidden');
    
    gsap.from(targetTab, {
        opacity: 0,
        y: 20,
        duration: 0.5,
        ease: 'power2.out'
    });
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initThree();
    animate();
    window.addEventListener('resize', onWindowResize);

    // Показываем начальную вкладку
    showTab('routes');

    // Обработка формы авторизации
    document.getElementById('authForm').addEventListener('submit', (e) => {
        e.preventDefault();
        // Здесь будет логика авторизации/регистрации
    });
});

