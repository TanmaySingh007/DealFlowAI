from django.core.management.base import BaseCommand
from deals.models import Company
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add 500 diverse companies to the database'

    def handle(self, *args, **options):
        # Company name templates for different industries
        company_templates = {
            'software': [
                'TechFlow', 'DataSync', 'CloudCore', 'DevStack', 'CodeCraft', 'AppLogic', 'ByteBridge', 'PixelPro', 'WebWave', 'SoftSphere',
                'DigitalDynamics', 'InnovateTech', 'SmartSolutions', 'FutureCode', 'EliteEngine', 'PrimePlatform', 'CoreSystems', 'NextGen', 'TechTrail', 'LogicLabs',
                'CodeCanvas', 'DevDream', 'AppArch', 'WebWorks', 'SoftServe', 'TechTonic', 'DataDriven', 'CloudConnect', 'InnovateIO', 'SmartStack'
            ],
            'fintech': [
                'PayFlow', 'MoneyMesh', 'CryptoCore', 'BankBridge', 'FinanceFlow', 'WealthWave', 'InvestIQ', 'CashConnect', 'TradeTech', 'LendLogic',
                'DigitalDollar', 'SmartPay', 'FutureFinance', 'EliteExchange', 'PrimePay', 'CoreCapital', 'NextMoney', 'FinanceFirst', 'WealthWise', 'TradeTrail',
                'PayPro', 'MoneyMint', 'CryptoCash', 'BankByte', 'FinanceFusion', 'WealthWorks', 'InvestInsight', 'CashCore', 'TradeTech', 'LendLink'
            ],
            'healthcare': [
                'MedTech', 'HealthHub', 'BioBridge', 'CareCore', 'WellnessWave', 'PharmaFlow', 'VitalView', 'MedMesh', 'HealthHero', 'BioByte',
                'DigitalHealth', 'SmartCare', 'FutureMed', 'EliteHealth', 'PrimeCare', 'CoreClinic', 'NextHealth', 'MedFirst', 'HealthWise', 'CareTrail',
                'MedPro', 'HealthHub', 'BioBridge', 'CareCore', 'WellnessWave', 'PharmaFlow', 'VitalView', 'MedMesh', 'HealthHero', 'BioByte'
            ],
            'energy': [
                'GreenGrid', 'SolarSync', 'WindWave', 'EcoEnergy', 'PowerPro', 'RenewableRise', 'CleanCore', 'EnergyEdge', 'SustainableSync', 'GreenGen',
                'DigitalEnergy', 'SmartSolar', 'FutureFuel', 'EliteEnergy', 'PrimePower', 'CoreClean', 'NextEnergy', 'GreenFirst', 'EnergyWise', 'PowerTrail',
                'EnergyPro', 'GreenGrid', 'SolarSync', 'WindWave', 'EcoEnergy', 'PowerPro', 'RenewableRise', 'CleanCore', 'EnergyEdge', 'SustainableSync'
            ],
            'education': [
                'EduTech', 'LearnLogic', 'SkillSync', 'KnowledgeCore', 'StudyStream', 'EduWave', 'LearnLink', 'SkillSphere', 'KnowledgeKey', 'StudySmart',
                'DigitalEdu', 'SmartLearn', 'FutureSkill', 'EliteEdu', 'PrimeLearn', 'CoreKnowledge', 'NextEdu', 'LearnFirst', 'SkillWise', 'StudyTrail',
                'EduPro', 'LearnLogic', 'SkillSync', 'KnowledgeCore', 'StudyStream', 'EduWave', 'LearnLink', 'SkillSphere', 'KnowledgeKey', 'StudySmart'
            ],
            'retail': [
                'RetailRise', 'ShopSync', 'MarketMesh', 'StoreStream', 'CommerceCore', 'RetailWave', 'ShopSmart', 'MarketMagic', 'StoreSync', 'CommerceConnect',
                'DigitalRetail', 'SmartShop', 'FutureMarket', 'EliteRetail', 'PrimeStore', 'CoreCommerce', 'NextRetail', 'ShopFirst', 'MarketWise', 'StoreTrail',
                'RetailPro', 'ShopSync', 'MarketMesh', 'StoreStream', 'CommerceCore', 'RetailWave', 'ShopSmart', 'MarketMagic', 'StoreSync', 'CommerceConnect'
            ],
            'logistics': [
                'LogiTech', 'ShipSync', 'DeliverDynamics', 'TransportTech', 'SupplySync', 'LogiWave', 'ShipSmart', 'DeliverDirect', 'TransportTrail', 'SupplyStream',
                'DigitalLogi', 'SmartShip', 'FutureDeliver', 'EliteLogi', 'PrimeTransport', 'CoreSupply', 'NextLogi', 'ShipFirst', 'DeliverWise', 'TransportTrail',
                'LogiPro', 'ShipSync', 'DeliverDynamics', 'TransportTech', 'SupplySync', 'LogiWave', 'ShipSmart', 'DeliverDirect', 'TransportTrail', 'SupplyStream'
            ],
            'cybersecurity': [
                'SecureSync', 'CyberCore', 'GuardGrid', 'ShieldStream', 'ProtectPro', 'SecureWave', 'CyberConnect', 'GuardGate', 'ShieldSmart', 'ProtectPath',
                'DigitalSecure', 'SmartCyber', 'FutureGuard', 'EliteSecure', 'PrimeProtect', 'CoreShield', 'NextSecure', 'CyberFirst', 'GuardWise', 'ShieldTrail',
                'SecurePro', 'CyberCore', 'GuardGrid', 'ShieldStream', 'ProtectPro', 'SecureWave', 'CyberConnect', 'GuardGate', 'ShieldSmart', 'ProtectPath'
            ],
            'ai_ml': [
                'AITech', 'MLMesh', 'NeuralNet', 'BrainByte', 'SmartAI', 'AIWave', 'MLMagic', 'NeuralNode', 'BrainBridge', 'SmartSync',
                'DigitalAI', 'SmartML', 'FutureBrain', 'EliteAI', 'PrimeML', 'CoreNeural', 'NextAI', 'BrainFirst', 'MLWise', 'SmartTrail',
                'AIPro', 'MLMesh', 'NeuralNet', 'BrainByte', 'SmartAI', 'AIWave', 'MLMagic', 'NeuralNode', 'BrainBridge', 'SmartSync'
            ],
            'other': [
                'InnovateIO', 'FutureFlow', 'EliteEdge', 'PrimePath', 'CoreConnect', 'NextNode', 'FirstFlow', 'WiseWave', 'TrailTech', 'ProPath',
                'DigitalDynamics', 'SmartSync', 'FutureFirst', 'EliteEdge', 'PrimePath', 'CoreConnect', 'NextNode', 'FirstFlow', 'WiseWave', 'TrailTech',
                'InnovatePro', 'FutureFlow', 'EliteEdge', 'PrimePath', 'CoreConnect', 'NextNode', 'FirstFlow', 'WiseWave', 'TrailTech', 'ProPath'
            ]
        }

        # Industry descriptions
        industry_descriptions = {
            'software': [
                'Leading software development company specializing in enterprise solutions',
                'Innovative SaaS platform for business automation',
                'Cloud-based software services for modern enterprises',
                'Cutting-edge software development and consulting services',
                'Enterprise software solutions for digital transformation',
                'Next-generation software platform for scalable applications',
                'Advanced software engineering and development services',
                'Innovative software solutions for industry 4.0',
                'Cloud-native software development company',
                'Enterprise-grade software platform provider'
            ],
            'fintech': [
                'Revolutionary fintech platform for digital payments',
                'Innovative financial technology solutions',
                'Digital banking and payment processing services',
                'Blockchain-based financial technology company',
                'AI-powered financial services platform',
                'Digital asset management and trading platform',
                'Mobile banking and financial services provider',
                'Cryptocurrency and digital payment solutions',
                'Regulatory technology and compliance platform',
                'Peer-to-peer lending and investment platform'
            ],
            'healthcare': [
                'Digital health technology and telemedicine platform',
                'AI-powered healthcare diagnostics and monitoring',
                'Medical device technology and innovation',
                'Healthcare data analytics and insights platform',
                'Digital therapeutics and health management',
                'Medical imaging and diagnostic technology',
                'Healthcare workflow automation and optimization',
                'Patient engagement and care coordination platform',
                'Healthcare cybersecurity and data protection',
                'Precision medicine and personalized healthcare'
            ],
            'energy': [
                'Renewable energy technology and solar solutions',
                'Smart grid and energy management systems',
                'Energy storage and battery technology',
                'Clean energy infrastructure and development',
                'Energy efficiency and sustainability solutions',
                'Wind power technology and development',
                'Electric vehicle charging infrastructure',
                'Carbon capture and climate technology',
                'Energy trading and market optimization',
                'Microgrid and distributed energy systems'
            ],
            'education': [
                'EdTech platform for online learning and education',
                'AI-powered personalized learning solutions',
                'Digital skills training and certification platform',
                'Educational content creation and distribution',
                'Student engagement and learning analytics',
                'Virtual reality and immersive learning technology',
                'Language learning and communication platform',
                'Corporate training and professional development',
                'Educational assessment and testing technology',
                'Learning management and course delivery platform'
            ],
            'retail': [
                'E-commerce platform and digital retail solutions',
                'Omnichannel retail technology and integration',
                'Retail analytics and customer insights platform',
                'Inventory management and supply chain optimization',
                'Digital marketing and customer engagement',
                'Point-of-sale and payment processing systems',
                'Retail automation and robotics technology',
                'Customer experience and loyalty platform',
                'Retail cybersecurity and fraud prevention',
                'Sustainable retail and circular economy solutions'
            ],
            'logistics': [
                'Supply chain optimization and logistics technology',
                'Last-mile delivery and logistics automation',
                'Freight management and transportation platform',
                'Warehouse automation and robotics technology',
                'Logistics analytics and route optimization',
                'International shipping and customs technology',
                'Fleet management and vehicle tracking systems',
                'Cold chain logistics and temperature monitoring',
                'E-commerce fulfillment and order processing',
                'Sustainable logistics and green transportation'
            ],
            'cybersecurity': [
                'Advanced cybersecurity and threat detection',
                'Zero-trust security architecture and implementation',
                'Cloud security and data protection platform',
                'Identity and access management solutions',
                'Security operations and incident response',
                'Network security and firewall technology',
                'Application security and code analysis',
                'IoT security and device protection',
                'Compliance and regulatory security solutions',
                'Penetration testing and security assessment'
            ],
            'ai_ml': [
                'Machine learning and artificial intelligence platform',
                'Natural language processing and text analytics',
                'Computer vision and image recognition technology',
                'Predictive analytics and data science platform',
                'AI-powered automation and robotics',
                'Deep learning and neural network solutions',
                'AI ethics and responsible technology',
                'Conversational AI and chatbot platform',
                'AI-powered business intelligence and analytics',
                'Autonomous systems and self-driving technology'
            ],
            'other': [
                'Innovative technology solutions for emerging markets',
                'Cross-industry digital transformation platform',
                'Specialized consulting and advisory services',
                'Research and development technology company',
                'Emerging technology incubator and accelerator',
                'Industry-specific digital solutions provider',
                'Technology consulting and implementation services',
                'Innovation lab and technology research center',
                'Digital strategy and transformation consulting',
                'Technology-enabled business process optimization'
            ]
        }

        # Cities for headquarters
        cities = [
            'San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA', 'Boston, MA',
            'Los Angeles, CA', 'Chicago, IL', 'Denver, CO', 'Atlanta, GA', 'Miami, FL',
            'Portland, OR', 'Nashville, TN', 'Charlotte, NC', 'Phoenix, AZ', 'Dallas, TX',
            'Houston, TX', 'Philadelphia, PA', 'San Diego, CA', 'Detroit, MI', 'Minneapolis, MN',
            'Salt Lake City, UT', 'Raleigh, NC', 'Columbus, OH', 'Indianapolis, IN', 'Kansas City, MO',
            'Pittsburgh, PA', 'Cleveland, OH', 'Cincinnati, OH', 'Milwaukee, WI', 'St. Louis, MO'
        ]

        # Website domains
        domains = [
            'techflow.com', 'datasync.io', 'cloudcore.tech', 'devstack.ai', 'codecraft.dev',
            'applogic.com', 'bytebridge.io', 'pixelpro.tech', 'webwave.com', 'softsphere.ai',
            'digitaldynamics.io', 'innovatetech.com', 'smartsolutions.ai', 'futurecode.dev', 'eliteengine.io',
            'primeplatform.com', 'coresystems.ai', 'nextgen.tech', 'techtrail.io', 'logiclabs.com',
            'codecanvas.dev', 'devdream.io', 'apparch.com', 'webworks.ai', 'softserve.tech',
            'techtonic.io', 'datadriven.com', 'cloudconnect.ai', 'innovateio.dev', 'smartstack.tech'
        ]

        created_count = 0
        existing_count = Company.objects.count()
        
        self.stdout.write(f"Starting with {existing_count} existing companies...")

        for i in range(500):
            # Select random industry
            industry = random.choice(list(company_templates.keys()))
            
            # Generate company name
            name_template = random.choice(company_templates[industry])
            suffix = random.choice(['', ' Inc', ' Corp', ' LLC', ' Technologies', ' Solutions', ' Systems', ' Labs', ' Group', ' International'])
            company_name = f"{name_template}{suffix}"
            
            # Check if company already exists
            if Company.objects.filter(name=company_name).exists():
                continue
            
            # Generate description
            description = random.choice(industry_descriptions[industry])
            
            # Generate other fields
            revenue_range = random.choice(['under_1m', '1_5m', '5_20m', '20_100m', '100m_plus'])
            funding_stage = random.choice(['seed', 'series_a', 'series_b', 'series_c', 'series_d', 'ipo', 'public', 'private'])
            
            # Generate founding year (between 1990 and 2023)
            founding_year = random.randint(1990, 2023)
            
            # Generate employee count based on funding stage
            if funding_stage in ['seed', 'series_a']:
                employee_count = random.randint(5, 50)
            elif funding_stage in ['series_b', 'series_c']:
                employee_count = random.randint(50, 200)
            elif funding_stage in ['series_d', 'ipo']:
                employee_count = random.randint(200, 1000)
            else:
                employee_count = random.randint(10, 500)
            
            # Generate total funding based on funding stage
            if funding_stage == 'seed':
                total_funding = Decimal(random.uniform(0.1, 2.0))
            elif funding_stage == 'series_a':
                total_funding = Decimal(random.uniform(2.0, 15.0))
            elif funding_stage == 'series_b':
                total_funding = Decimal(random.uniform(15.0, 50.0))
            elif funding_stage == 'series_c':
                total_funding = Decimal(random.uniform(50.0, 150.0))
            elif funding_stage == 'series_d':
                total_funding = Decimal(random.uniform(150.0, 500.0))
            else:
                total_funding = Decimal(random.uniform(10.0, 1000.0))
            
            # Generate website
            domain = random.choice(domains)
            website = f"https://www.{domain}"
            
            # Generate headquarters
            headquarters = random.choice(cities)
            
            # Generate similarity score (for ML matching)
            similarity_score = round(random.uniform(0.1, 0.95), 3)
            
            try:
                company = Company.objects.create(
                    name=company_name,
                    description=description,
                    industry=industry,
                    revenue_range=revenue_range,
                    funding_stage=funding_stage,
                    website=website,
                    founding_year=founding_year,
                    employee_count=employee_count,
                    headquarters=headquarters,
                    total_funding=total_funding,
                    similarity_score=similarity_score,
                    is_active=True
                )
                created_count += 1
                
                if created_count % 50 == 0:
                    self.stdout.write(f"Created {created_count} companies...")
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating company {company_name}: {e}"))
                continue
        
        final_count = Company.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new companies. '
                f'Total companies in database: {final_count}'
            )
        ) 