import React from 'react';
import { Phone, Mail, Store } from 'lucide-react';

const ContactUs: React.FC = () => {
  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Contact Us</h1>
      <div className="bg-white rounded-lg shadow-md p-6 flex flex-col md:flex-row gap-8 items-start">
        <div className="flex-1 space-y-6">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-3 rounded-full">
              <Store className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">LT store - Living with love</h2>
              <p className="text-gray-600">Grocery Store</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-green-100 p-3 rounded-full">
              <Phone className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Phone</h3>
              <p className="text-lg">+855 61 755 859</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-purple-100 p-3 rounded-full">
              <Mail className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Email</h3>
              <a href="mailto:lengkundee01@gmail.com" className="text-lg text-blue-600 hover:underline">
                lengkundee01@gmail.com
              </a>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100">
            <p className="text-gray-600">
              Connect with us on our Facebook page for the latest updates and offers!
            </p>
          </div>
        </div>

        <div className="flex-1 bg-gray-50 p-4 rounded-lg w-full max-w-md">
          <img
            src="/facebook_page.jpg"
            alt="LT Store Facebook Page"
            className="w-full rounded-md shadow-sm border border-gray-200"
          />
        </div>
      </div>
    </div>
  );
};

export default ContactUs;
