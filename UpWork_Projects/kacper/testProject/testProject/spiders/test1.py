import scrapy
from urllib.parse import urljoin


class Test1Spider(scrapy.Spider):
    name = 'test1'
    
    def start_requests(self):
        yield scrapy.Request(
            url="http://phonedb.net/index.php?m=device&s=list&filter=0",
            callback=self.getPhoneUrls
        )

    def getPhoneUrls(self, response):
        cntr = 0
        while True:
            cntr += 29
            phones = response.xpath("//div[@class='container']/div[@class='content_block']/div[@class='content_desc']/following-sibling::a[1]")
            for phone in phones:
                yield scrapy.Request(
                    url=urljoin(response.url, phone.xpath(".//@href").get()),
                    callback=self.parse
                )
            if cntr <= 17748:
                yield scrapy.Request(
                    url=f"http://phonedb.net/index.php?m=device&s=list&filter={cntr}",
                    callback=self.getPhoneUrls
                )            
            else:
                break

    def parse(self, response):
        yield {
            'Introduction': {
                'Brand': response.xpath("normalize-space(//strong[contains(text(), 'Brand')]/parent::td/following-sibling::td/a/text())").get(),
                'Model': response.xpath("normalize-space(//strong[contains(text(), 'Model')]/parent::td/following-sibling::td/text())").get(),
                'Released': response.xpath("normalize-space(//strong[contains(text(), 'Released')]/parent::td/following-sibling::td/text())").get(),
                'Announced': response.xpath("normalize-space(//strong[contains(text(), 'Announced')]/parent::td/following-sibling::td/text())").get(),
                'Hardware Designer': response.xpath("normalize-space(//strong[contains(text(), 'Hardware Designer')]/parent::td/following-sibling::td/a/text())").get(),
                'Manufacturer': response.xpath("normalize-space(//strong[contains(text(), 'Manufacturer')]/parent::td/following-sibling::td/a/text())").get(),
                'Codename': response.xpath("normalize-space(//strong[contains(text(), 'Codename')]/parent::td/following-sibling::td/a/text())").get(),
                'OEM ID': response.xpath("normalize-space(//strong[contains(text(), 'OEM ID')]/parent::td/following-sibling::td/a/text())").get(),
                'General Extras': response.xpath("normalize-space(//strong[contains(text(), 'General Extras')]/parent::td/following-sibling::td/a/text())").get(),
                'Device Category': response.xpath("normalize-space(//strong[contains(text(), 'Device Category')]/parent::td/following-sibling::td/a/text())").get(),
                'List of Additional Features': response.xpath("normalize-space(//strong[text()='List of Additional Features']/parent::td/following-sibling::td/text())").get(),
            },
            'Physical Attributes': {
                'Width (mm)': response.xpath("normalize-space(//strong[text()='Width']/parent::td/following-sibling::td/a/text())").get(),
                'Width (inch)': response.xpath("normalize-space(//strong[text()='Width']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(), 'inch')]/text())").get(),
                'Height (mm)': response.xpath("normalize-space(//strong[contains(text(), 'Height')]/parent::td/following-sibling::td/a/text())").get(),
                'Height (inch)': response.xpath("normalize-space(//strong[text()='Height']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(), 'inch')]/text())").get(),
                'Depth (mm)': response.xpath("normalize-space(//strong[contains(text(), 'Depth')]/parent::td/following-sibling::td/a/text())").get(),
                'Depth (inch)': response.xpath("normalize-space(//strong[text()='Depth']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(), 'inch')]/text())").get(),
                'Dimensions': response.xpath("normalize-space(//td[contains(text(), 'Dimensions')]/following-sibling::td/text())").get(),
                'Bounding Volume': response.xpath("normalize-space(//strong[text()='Bounding Volume']/parent::td/following-sibling::td/text())").get(),
                'Mass in grams': response.xpath("normalize-space(//strong[contains(text(), 'Mass')]/parent::td/following-sibling::td/a/text())").get(),
                'Mass in ounces': response.xpath("normalize-space(//td[contains(text(),'ounces')]/text())").get()
            },
            'Software Environment': {
                'Platform': response.xpath("normalize-space(//strong[contains(text(), 'Platform')]/parent::td/following-sibling::td/a/text())").get(),
                'Operating System': response.xpath("normalize-space(//strong[contains(text(), 'Operating System')]/parent::td/following-sibling::td/a/text())").get(),
                'Platform': response.xpath("//strong[contains(text(), 'Software Extras')]/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Application processor, Chipset': {
                'CPU Clock': response.xpath("normalize-space(//strong[contains(text(), 'CPU Clock')]/parent::td/following-sibling::td/a/text())").get(),
                'CPU': response.xpath("normalize-space(//strong[text()='CPU']/parent::td/following-sibling::td/a/text())").get()
            },
            'Operative Memory': {
                'RAM Type': response.xpath("normalize-space(//strong[text()='RAM Type']/parent::td/following-sibling::td/a/text())").get(),
                'RAM Frequency': response.xpath("normalize-space(//strong[text()='RAM Type']/parent::td/parent::tr/following-sibling::tr//a[contains(text(), 'MHz')]/text())").get(),
                'RAM Capacity (converted)': response.xpath("normalize-space(//strong[contains(text(), 'RAM Capacity')]/parent::td/following-sibling::td/a/text())").get()
            },
            'Non-volatile Memory': {
                'Non-volatile Memory Type': response.xpath("normalize-space(//strong[contains(text(), 'Non-volatile Memory Type')]/parent::td/following-sibling::td/a/text())").get(),
                'Non-volatile Memory Capacity (converted)': response.xpath("normalize-space(//strong[contains(text(), 'Non-volatile Memory Capacity')]/parent::td/following-sibling::td/a/text())").get(),
            },
            'Display': {
                'Display Notch': response.xpath("normalize-space(//strong[contains(text(), 'Display Notch')]/parent::td/following-sibling::td/a/text())").get(),
                'Display Diagonal (mm)': response.xpath("normalize-space(//strong[contains(text(), 'Display Diagonal')]/parent::td/following-sibling::td/text())").get(),
                'Display Diagonal (inch)': response.xpath("normalize-space(//strong[text()='Display Diagonal']/parent::td/parent::tr/following-sibling::tr//a[contains(text(), 'inch')]/text())").get(),
                'Resolution': response.xpath("normalize-space(//strong[text()='Resolution']/parent::td/following-sibling::td/text())").get(),
                'Resolution (pixels)': response.xpath("normalize-space(//strong[text()='Resolution']/parent::td/parent::tr/following-sibling::tr/td[contains(text(), 'pixels')]/text())").get(),
                'Display Width (mm)': response.xpath("normalize-space(//strong[text()='Display Width']/parent::td/following-sibling::td/text())").get(),
                'Display Width (inch)': response.xpath("normalize-space(//strong[text()='Display Width']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(), 'inch')]/text())").get(),
                'Display Height (mm)': response.xpath("normalize-space(//strong[text()='Display Height']/parent::td/following-sibling::td/text())").get(),
                'Display Height (inch)': response.xpath("normalize-space(//strong[text()='Display Height']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(), 'inch')]/text())").get(),
                'Horizontal Full Bezel Width': response.xpath("normalize-space(//strong[text()='Horizontal Full Bezel Width']/parent::td/following-sibling::td/a/text())").get(),
                'Display Area': response.xpath("normalize-space(//strong[text()='Display Area']/parent::td/following-sibling::td/text())").get(),
                'Display Area Utilization': response.xpath("normalize-space(//strong[text()='Display Area Utilization']/parent::td/following-sibling::td/a/text())").get(),
                'Pixel Size': response.xpath("normalize-space(//strong[text()='Pixel Size']/parent::td/following-sibling::td/text())").get(),
                'Pixel Density': response.xpath("normalize-space(//strong[text()='Pixel Density']/parent::td/following-sibling::td/a/text())").get(),
                'Display Type': response.xpath("normalize-space(//strong[text()='Display Type']/parent::td/following-sibling::td/a/text())").get(),
                'Display Subtype': response.xpath("normalize-space(//td[text()='Display Subtype']/following-sibling::td/a/text())").get(),
                'Number of Display Scales': response.xpath("normalize-space(//strong[text()='Number of Display Scales']/parent::td/following-sibling::td/text())").get(),
                'Display Dynamic Range Depth': response.xpath("normalize-space(//strong[text()='Display Dynamic Range Depth']/parent::td/following-sibling::td/a/text())").get(),
                'Display Illumination': response.xpath("normalize-space(//strong[text()='Display Illumination']/parent::td/following-sibling::td/a/text())").get(),
                'Display Light Reflection Mode': response.xpath("normalize-space(//strong[text()='Display Light Reflection Mode']/parent::td/following-sibling::td/a/text())").get(),
                'Display Subpixel Scheme': response.xpath("normalize-space(//strong[text()='Display Subpixel Scheme']/parent::td/following-sibling::td/a/text())").get(),                
                'Display Refresh Rate': response.xpath("normalize-space(//strong[text()='Display Refresh Rate']/parent::td/following-sibling::td/a/text())").get(),
                'Scratch Resistant Screen': response.xpath("normalize-space(//strong[text()='Scratch Resistant Screen']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Graphical Subsystem': {
                'Graphical Controller': response.xpath("normalize-space(//strong[text()='Graphical Controller']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Audio/Video Interfaces': {
                'A/V Out': response.xpath("normalize-space(//strong[text()='A/V Out']/parent::td/following-sibling::td/a/text())").get(),
                'A/V Out (Type)': response.xpath("normalize-space(//strong[text()='A/V Out']/parent::td/parent::tr/following-sibling::tr[1]//a/text())").get(),
                'A/V Out Max. Resolution': response.xpath("normalize-space(//strong[text()='A/V Out Max. Resolution']/parent::td/following-sibling::td/text())").get(),
            },
            'Audio Subsystem': {
                'Audio Channel(s)': response.xpath("normalize-space(//strong[text()='Audio Channel(s)']/parent::td/following-sibling::td/a/text())").get(),
                'Audio Controller': response.xpath("normalize-space(//td[text()='Audio Controller']/following-sibling::td/a/text())").get(),
            },
            'Sound Recording': {
                'Microphone(s)': response.xpath("normalize-space(//strong[text()='Microphone(s)']/parent::td/following-sibling::td/a/text())").get(),
                'Microphone Input': response.xpath("normalize-space(//strong[text()='Microphone Input']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Sound Playing': {
                'Loudpeaker(s)': response.xpath("normalize-space(//strong[text()='Loudpeaker(s)']/parent::td/following-sibling::td/a/text())").get(),
                'Audio Output': response.xpath("normalize-space(//strong[text()='Audio Output']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Cellular Phone': {
                'Supported Cellular Bands': response.xpath("//strong[text()='Supported Cellular Bands']/parent::td/following-sibling::td/a/text()").getall(),
                'Supported Cellular Data Links': response.xpath("//strong[text()='Supported Cellular Data Links']/parent::td/following-sibling::td/a/text()").getall(),
                'SIM Card Slot': response.xpath("normalize-space(//strong[text()='SIM Card Slot']/parent::td/following-sibling::td/a/text())").get(),
                'Cellular Antenna': response.xpath("normalize-space(//strong[text()='Cellular Antenna']/parent::td/following-sibling::td/text())").get(),
                'Call Alert Sound': response.xpath("normalize-space(//strong[text()='Call Alert Sound']/parent::td/following-sibling::td/a/text())").get(),
                'Hearing Aid Compatibility': response.xpath("//strong[text()='Hearing Aid Compatibility (HAC)']/parent::td/following-sibling::td/a/text()").getall(),
                'Complementary Phone Services': response.xpath("//strong[text()='Complementary Phone Services']/parent::td/following-sibling::td/a/text()").getall(),
                'Cellular Controller': response.xpath("normalize-space(//strong[text()='Cellular Controller']/parent::td/following-sibling::td/a/text())").get(),
                'SAR (head)': response.xpath("normalize-space(//strong[text()='SAR (head)']/parent::td/following-sibling::td/text())").get(),
                'SAR (head) Desc': response.xpath("//strong[text()='SAR (head)']/parent::td/parent::tr/following-sibling::tr[1]/td/text()").getall(),
                'SAR (body)': response.xpath("normalize-space(//strong[text()='SAR (body)']/parent::td/following-sibling::td/text())").get(),
                'SAR (body) Desc': response.xpath("//strong[text()='SAR (body)']/parent::td/parent::tr/following-sibling::tr[1]/td/text()").getall(),
                '2nd highest SAR (head)': response.xpath("normalize-space(//strong[text()='2nd highest SAR (head)']/parent::td/following-sibling::td/text())").get(),
                '2nd highest SAR (head) Desc': response.xpath("//strong[text()='2nd highest SAR (head)']/parent::td/parent::tr/following-sibling::tr[1]/td/text()").getall(),
                '2nd highest SAR (body)': response.xpath("normalize-space(//strong[text()='2nd highest SAR (body)']/parent::td/following-sibling::td/text())").get(),
                '2nd highest SAR (body) Desc': response.xpath("//strong[text()='2nd highest SAR (body)']/parent::td/parent::tr/following-sibling::tr[1]/td/text()").getall(),
            },
            'Secondary Cellular Phone': {
                'Dual Cellular Network Operation': response.xpath("normalize-space(//strong[text()='Dual Cellular Network Operation']/parent::td/following-sibling::td/a/text())").get(),
                'Sec Supported Cellular Networks': response.xpath("//strong[text()='Sec. Supported Cellular Networks']/parent::td/following-sibling::td/text()").getall(),
                'Sec Supported Cellular Data Links': response.xpath("//strong[text()='Sec. Supported Cellular Data Links']/parent::td/following-sibling::td/text()").getall(),
                'Sec SIM Card Slot': response.xpath("normalize-space(//strong[text()='Sec. SIM Card Slot']/parent::td/following-sibling::td/a/text())").get(),
                'Sec Cellular Antenna': response.xpath("normalize-space(//strong[text()='Sec. SIM Card Slot']/parent::td/parent::tr/following-sibling::tr[1]/td/text())").get()
            },
            'Control Peripherals': {
                'Touchscreen Type': response.xpath("normalize-space(//strong[text()='Touchscreen Type']/parent::td/following-sibling::td/a/text())").get(),
                'Touchscreen Simultaneous Touch Points': response.xpath("normalize-space(//strong[text()='Touchscreen Simultaneous Touch Points']/parent::td/following-sibling::td/a/text())").get(),
                'Touchscreen Sampling rate': response.xpath("normalize-space(//strong[text()='Touchscreen Sampling rate']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Communication Interfaces': {
                'Expansion Interfaces': response.xpath("normalize-space(//strong[text()='Expansion Interfaces']/parent::td/following-sibling::td/text())").get(),
                'USB': response.xpath("normalize-space(//strong[text()='USB']/parent::td/following-sibling::td/a/text())").get(),
                'USB Features': response.xpath("//strong[text()='USB']/parent::td/parent::tr/following-sibling::tr[1]/td/a/text()").getall(),
                'USB Services': response.xpath("//td[text()='USB Services']/following-sibling::td/a/text()").getall(),
                'USB Connector': response.xpath("normalize-space(//td[text()='USB Connector']/following-sibling::td/a/text())").get(),
                'Max. Charging Power': response.xpath("normalize-space(//td[contains(text(),'Max. Charging Power')]/following-sibling::td/a/text())").get(),
                'Bluetooth': response.xpath("normalize-space(//strong[text()='Bluetooth']/parent::td/following-sibling::td/a/text())").get(),
                'Bluetooth Antenna': response.xpath("normalize-space(//strong[text()='Bluetooth']/parent::td/parent::tr/following-sibling::tr[1]/td/text())").get(),
                'Bluetooth profiles': response.xpath("//td[contains(text(),'Bluetooth profiles')]/following-sibling::td/a/text()").getall(),
                'Wireless LAN': response.xpath("//strong[text()='Wireless LAN']/parent::td/following-sibling::td/a/text()").getall(),
                'Wireless Antenna': response.xpath("normalize-space(//strong[text()='Wireless LAN']/parent::td/parent::tr/following-sibling::tr[1]/td/text())").get(),
                'Wireless Services': response.xpath("//td[contains(text(),'Wireless Services')]/following-sibling::td/a/text()").getall(),
                'NFC': response.xpath("//strong[text()='NFC']/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Multimedia Broadcast': {
                'FM Radio Receiver': response.xpath("normalize-space(//strong[text()='FM Radio Receiver']/parent::td/following-sibling::td/text())").get(),
            },
            'Satellite Navigation': {
                'Supported GPS protocol(s)': response.xpath("normalize-space(//strong[text()='Supported GPS protocol(s)']/parent::td/following-sibling::td/a/text())").get(),
                'GPS Antenna': response.xpath("normalize-space(//td[contains(text(),'GPS Antenna')]/following-sibling::td/text())").get(),
                'Complementary GPS Services': response.xpath("//strong[text()='Complementary GPS Services']/parent::td/following-sibling::td/a/text()").getall(),
                'Supported GLONASS protocol(s)': response.xpath("normalize-space(//strong[text()='Supported GLONASS protocol(s)']/parent::td/following-sibling::td/a/text())").get(),
                'Supported Galileo service(s)': response.xpath("normalize-space(//strong[text()='Supported Galileo service(s)']/parent::td/following-sibling::td/a/text())").get(),
                'Supported BeiDou system (BDS)': response.xpath("normalize-space(//strong[text()='Supported BeiDou system (BDS)']/parent::td/following-sibling::td/a/text())").get(),      
            },
            'Primary Camera System': {
                'Camera Placement': response.xpath("normalize-space(//strong[text()='Camera Placement']/parent::td/following-sibling::td/text())").get(),
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Camera Image Sensor']/parent::td/following-sibling::td/a/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Image Sensor Pixel Size']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Camera Resolution']/parent::td/following-sibling::td/text())").get(),
                'Number of effective pixels': response.xpath("normalize-space(//strong[text()='Number of effective pixels']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Optical Zoom': response.xpath("normalize-space(//strong[text()='Zoom']/parent::td/following-sibling::td/a/text())").get(),
                'Digital Zoom': response.xpath("normalize-space(//strong[text()='Zoom']/parent::td/parent::tr/following-sibling::tr[1]/td/a/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Focus']/parent::td/following-sibling::td/a/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Recordable Image Formats': response.xpath("//strong[text()='Recordable Image Formats']/parent::td/following-sibling::td/text()").getall(),
                'Video Recording': response.xpath("normalize-space(//strong[text()='Video Recording']/parent::td/following-sibling::td/text())").get(),
                'Video Recording (fps)': response.xpath("normalize-space(//strong[text()='Video Recording']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(),'fps')]/text())").get(),
                'Recordable Video Formats': response.xpath("//strong[text()='Recordable Video Formats']/parent::td/following-sibling::td/text()").getall(),
                'Flash': response.xpath("normalize-space(//strong[text()='Flash']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Camera Extra Functions']/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Auxilliary Camera': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Aux. Camera Image Sensor']/parent::td/following-sibling::td/a/text())").get(),
                'Cam Image Sensor Format': response.xpath("normalize-space(//strong[text()='Aux. Cam. Image Sensor Format']/parent::td/following-sibling::td/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Aux. Cam. Image Sensor Pixel Size']/parent::td/following-sibling::td/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Auxiliary Camera Resolution']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Aux. Camera Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Aux. Cam. Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Aux. Camera Focus']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Aux. Camera Extra Functions']/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Auxilliary Camera No. 2': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Aux. 2 Camera Image Sensor']/parent::td/following-sibling::td/a/text())").get(),
                'Cam Image Sensor Format': response.xpath("normalize-space(//strong[text()='Aux. 2 Cam. Image Sensor Format']/parent::td/following-sibling::td/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Aux. 2 Cam. Image Sensor Pixel Size']/parent::td/following-sibling::td/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Auxiliary 2 Camera Resolution']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Aux. 2 Camera Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Aux. 2 Cam. Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Aux. 2 Camera Focus']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Aux. 2 Camera Extra Functions']/parent::td/following-sibling::td/text()").getall()
            },
            'Auxilliary Camera No. 3': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Aux. 3 Camera Image Sensor']/parent::td/following-sibling::td/a/text())").get(),
                'Cam Image Sensor Format': response.xpath("normalize-space(//strong[text()='Aux. 3 Cam. Image Sensor Format']/parent::td/following-sibling::td/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Aux. 3 Cam. Image Sensor Pixel Size']/parent::td/following-sibling::td/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Auxiliary 3 Camera Resolution']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Aux. 3 Camera Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Aux. 3 Cam. Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Aux. 3 Camera Focus']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Aux. 3 Camera Extra Functions']/parent::td/following-sibling::td/text()").getall()
            },
            'Auxilliary Camera No. 4': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Aux. 4 Camera Image Sensor']/parent::td/following-sibling::td/text())").get(),
                'Cam Image Sensor Format': response.xpath("normalize-space(//strong[text()='Aux. 4 Cam. Image Sensor Format']/parent::td/following-sibling::td/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Aux. 4 Cam. Image Sensor Pixel Size']/parent::td/following-sibling::td/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Auxiliary 4 Camera Resolution']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Aux. 4 Camera Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Aux. 4 Cam. Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Aux. 4 Camera Focus']/parent::td/following-sibling::td/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Aux. 4 Camera Extra Functions']/parent::td/following-sibling::td/text()").getall()
            },
            'Secondary Camera System': {
                'Camera Placement': response.xpath("normalize-space(//strong[text()='Secondary Camera Placement']/parent::td/following-sibling::td/text())").get(),
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Secondary Camera Sensor']/parent::td/following-sibling::td/a/text())").get(),
                'Image Sensor Pixel Size': response.xpath("normalize-space(//strong[text()='Secondary Image Sensor Pixel Size']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Resolution': response.xpath("normalize-space(//strong[text()='Secondary Camera Resolution']/parent::td/following-sibling::td/text())").get(),
                'Number of effective pixels': response.xpath("normalize-space(//strong[text()='Secondary Number of effective pixels']/parent::td/following-sibling::td/a/text())").get(),
                'Aperture (W)': response.xpath("normalize-space(//strong[text()='Secondary Aperture (W)']/parent::td/following-sibling::td/text())").get(),
                'Optical Zoom': response.xpath("normalize-space(//strong[text()='Secondary Zoom']/parent::td/following-sibling::td/a/text())").get(),
                'Digital Zoom': response.xpath("normalize-space(//strong[text()='Secondary Zoom']/parent::td/parent::tr/following-sibling::tr[1]/td/a/text())").get(),
                'Focus': response.xpath("normalize-space(//strong[text()='Secondary Focus']/parent::td/following-sibling::td/a/text())").get(),
                'Min Equiv Focal Length': response.xpath("normalize-space(//strong[text()='Secondary Min. Equiv. Focal Length']/parent::td/following-sibling::td/text())").get(),
                'Recordable Image Formats': response.xpath("//strong[text()='Secondary Recordable Image Formats']/parent::td/following-sibling::td/text()").getall(),
                'Video Recording': response.xpath("normalize-space(//strong[text()='Secondary Video Recording']/parent::td/following-sibling::td/text())").get(),
                'Video Recording (fps)': response.xpath("normalize-space(//strong[text()='Secondary Video Recording']/parent::td/parent::tr/following-sibling::tr[1]/td[contains(text(),'fps')]/text())").get(),
                'Recordable Video Formats': response.xpath("//strong[text()='Secondary Recordable Video Formats']/parent::td/following-sibling::td/text()").getall(),
                'Flash': response.xpath("normalize-space(//strong[text()='Secondary Flash']/parent::td/following-sibling::td/a/text())").get(),
                'Camera Extra Functions': response.xpath("//strong[text()='Secondary Camera Extra Functions']/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Secondary Auxilliary Camera': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Sec. Aux. Cam. Image Sensor']/parent::td/following-sibling::td/a/text())").get(),
            },
            'Secondary Auxilliary Camera No 2': {
                'Camera Image Sensor': response.xpath("normalize-space(//strong[text()='Sec. Aux. 2 Cam. Image Sensor']/parent::td/following-sibling::td/text())").get(),
            },
            'Built-in Sensors': {
                'Built-in compass': response.xpath("normalize-space(//strong[text()='Built-in compass']/parent::td/following-sibling::td/a/text())").get(),
                'Built-in accelerometer': response.xpath("normalize-space(//strong[text()='Built-in accelerometer']/parent::td/following-sibling::td/a/text())").get(),
                'Built-in gyroscope': response.xpath("normalize-space(//strong[text()='Built-in gyroscope']/parent::td/following-sibling::td/a/text())").get(),
                'Additional sensors': response.xpath("//strong[text()='Additional sensors']/parent::td/following-sibling::td/a/text()").getall(),
            },
            'Ingress Protection': {
                'Protection from solid materials': response.xpath("normalize-space(//strong[text()='Protection from solid materials']/parent::td/following-sibling::td/a/text())").get(),
                'Protection from liquids': response.xpath("normalize-space(//strong[text()='Protection from liquids']/parent::td/following-sibling::td/a/text())").get(),
                'Immersion into liquids (depth limit)': response.xpath("normalize-space(//strong[text()='Immersion into liquids (depth limit)']/parent::td/following-sibling::td/a/text())").get(),
                'Immersion into liquids time limit': response.xpath("normalize-space(//strong[text()='Immersion into liquids time limit']/parent::td/following-sibling::td/text())").get(),
            },
            'Power Supply': {
                'Battery': response.xpath("normalize-space(//strong[text()='Battery']/parent::td/following-sibling::td/a/text())").get(),
                'Nominal Cell Voltage (1st cell)': response.xpath("normalize-space(//strong[text()='Nominal Cell Voltage (1st cell)']/parent::td/following-sibling::td/text())").get(),
                'Nominal Cell Capacity (1st cell)': response.xpath("normalize-space(//strong[text()='Nominal Cell Capacity (1st cell)']/parent::td/following-sibling::td/text())").get(),
                'Nominal Cell Voltage (2nd cell)': response.xpath("normalize-space(//strong[text()='Nominal Cell Voltage (2nd cell)']/parent::td/following-sibling::td/text())").get(),
                'Nominal Cell Capacity (2nd cell)': response.xpath("normalize-space(//strong[text()='Nominal Cell Capacity (2nd cell)']/parent::td/following-sibling::td/text())").get(),
                'Nominal Battery Voltage': response.xpath("normalize-space(//strong[text()='Nominal Battery Voltage']/parent::td/following-sibling::td/a/text())").get(),
                'Nominal Battery Capacity': response.xpath("normalize-space(//strong[text()='Nominal Battery Capacity']/parent::td/following-sibling::td/a/text())").get(),
                'Nominal Battery Energy': response.xpath("normalize-space(//strong[text()='Nominal Battery Energy']/parent::td/following-sibling::td/a/text())").get(),
                'Estimated Battery Life': response.xpath("normalize-space(//strong[text()='Estimated Battery Life']/parent::td/following-sibling::td/text())").get(),
                'Power Supply Controller IC': response.xpath("normalize-space(//strong[text()='Power Supply Controller IC']/parent::td/following-sibling::td/text())").get(),
                'Wireless Charging': response.xpath("//strong[text()='Wireless Charging']/parent::td/following-sibling::td/a/text()").getall(),
                'Max Wireless Charging Power': response.xpath("normalize-space(//td[contains(text(),'Max. Wireless Charging Power')]/following-sibling::td/a/text())").get(),
            },
            'Geographical Attributes': {
                'Market Countries': response.xpath("//strong[text()='Market Countries']/parent::td/following-sibling::td/a/text()").getall(),
                'Market Regions': response.xpath("//strong[text()='Market Regions']/parent::td/following-sibling::td/a/text()").getall(),
                'Mobile Operator': response.xpath("//strong[text()='Mobile Operator']/parent::td/following-sibling::td/a/text()").getall(),
                'Price': response.xpath("normalize-space(//strong[text()='Price']/parent::td/following-sibling::td/text())").get(),
                'Currency': response.xpath("normalize-space(//strong[text()='Price']/parent::td/parent::tr/following-sibling::tr[1]/td/text())").get(),
            },
            'Page Url': response.url
        }
        
